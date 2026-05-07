"""Budget and selection helpers for live review inputs."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from code_review_agent.models import (
    ContextRequest,
    EvidencePackage,
    ReviewEvidence,
    ReviewerContext,
    RiskSignal,
)


DEFAULT_CONTEXT_BUDGET_TOKENS = 24000
DEFAULT_MAX_FILES_PER_AGENT_CALL = 8
DEFAULT_MAX_EVIDENCE_PER_FILE = 80
DEFAULT_MAX_EVIDENCE_ITEMS = 400
DEFAULT_MAX_RISK_EVIDENCE_IDS = 5
LIVE_REVIEW_INPUT_SCHEMA = "live_review_input_v1"
SELECTION_STRATEGY = "risk_first_v1"
SHARDING_STRATEGY = "file_risk_shards_v1"
REFILL_STRATEGY = "one_shot_refill_v1"
ALLOWED_CONTEXT_REQUEST_TYPES = frozenset(
    {
        "same_file_more_evidence",
        "related_tests",
        "related_symbol",
        "risk_evidence",
    }
)

_HIGH_RISK_SCORE = {
    "security_sensitive": 100.0,
    "api_change": 90.0,
    "error_handling_change": 85.0,
    "dependency_change": 70.0,
    "config_change": 70.0,
    "test_gap": 65.0,
    "behavior_change": 60.0,
    "design_constraint_violation": 50.0,
    "experiment_artifact": 40.0,
}
_KIND_SCORE = {
    "risk": 55.0,
    "diff": 45.0,
    "entity": 40.0,
    "test_discovery": 25.0,
    "hygiene": 15.0,
}


@dataclass(slots=True)
class SelectedEvidenceAudit:
    """Selection audit entry local to the live context builder."""

    evidence_id: str
    status: str
    score: float
    reason: str
    estimated_tokens: int
    source: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "status": self.status,
            "score": self.score,
            "reason": self.reason,
            "estimated_tokens": self.estimated_tokens,
            "source": self.source,
        }


@dataclass(slots=True)
class LiveReviewInput:
    """A single LLM-facing payload plus local audit data."""

    payload: dict[str, Any]
    context_budget: dict[str, Any]
    reviewer_context: ReviewerContext
    selected_evidence: list[SelectedEvidenceAudit] = field(default_factory=list)
    omitted_evidence: list[SelectedEvidenceAudit] = field(default_factory=list)


def estimate_tokens(value: object) -> int:
    """Estimate token count without adding a tokenizer runtime dependency."""

    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return max(1, len(text) // 4)


def score_evidence(package: EvidencePackage, evidence_id: str) -> float:
    """Return a deterministic usefulness score for one evidence item."""

    evidence = package.evidence_index.get(evidence_id)
    score = _KIND_SCORE.get(evidence.kind if evidence else "", 5.0)
    path = _path_for_evidence(evidence_id, evidence)

    for signal in package.risk_signals:
        risk_score = _HIGH_RISK_SCORE.get(signal.tag, 35.0)
        if evidence_id in signal.evidence_ids:
            score = max(score, risk_score + 20.0)
        if evidence_id.startswith(f"risk:{signal.tag}:"):
            score = max(score, risk_score + 10.0)
        if path and any(_evidence_path(item) == path for item in signal.evidence_ids):
            score = max(score, risk_score)

    if evidence_id.startswith("diff:"):
        score += 5.0
    if evidence_id.startswith("entity:"):
        score += 3.0
    return score


def build_live_review_input(
    package: EvidencePackage,
    *,
    max_input_tokens: int = DEFAULT_CONTEXT_BUDGET_TOKENS,
    max_files: int = DEFAULT_MAX_FILES_PER_AGENT_CALL,
    max_evidence_per_file: int = DEFAULT_MAX_EVIDENCE_PER_FILE,
    max_evidence_items: int = DEFAULT_MAX_EVIDENCE_ITEMS,
    allowed_paths: set[str] | None = None,
    forced_evidence_ids: set[str] | None = None,
    shard_id: str = "shard-001",
    shard_index: int = 0,
    shard_count: int = 1,
    is_refill: bool = False,
    parent_shard_id: str | None = None,
    request_types: list[str] | None = None,
) -> LiveReviewInput:
    """Build a single budgeted LLM-facing input from a full EvidencePackage."""

    max_input_tokens = max(1, max_input_tokens)
    max_files = max(1, max_files)
    max_evidence_per_file = max(1, max_evidence_per_file)
    max_evidence_items = max(1, max_evidence_items)

    selected: list[SelectedEvidenceAudit] = []
    omitted: list[SelectedEvidenceAudit] = []
    selected_index: dict[str, ReviewEvidence] = {}
    selected_ids: set[str] = set()
    per_file_counts: dict[str, int] = {}
    warnings: list[str] = []

    base_payload = _base_payload(package, max_files=max_files, allowed_paths=allowed_paths)
    used_tokens = estimate_tokens(base_payload)
    candidate_ids = _ranked_candidate_ids(
        package,
        allowed_paths=allowed_paths,
        forced_evidence_ids=forced_evidence_ids,
    )

    for evidence_id in candidate_ids:
        if forced_evidence_ids is not None and evidence_id not in forced_evidence_ids:
            continue
        evidence = package.evidence_index[evidence_id]
        audit = _audit_entry(
            package,
            evidence_id,
            status="selected",
            reason=_selection_reason(package, evidence_id),
        )
        path = _path_for_evidence(evidence_id, evidence) or "<unknown>"
        per_file_count = per_file_counts.get(path, 0)
        projected = used_tokens + estimate_tokens(evidence.to_dict())
        omit_reason = _omit_reason(
            projected=projected,
            max_input_tokens=max_input_tokens,
            selected_count=len(selected),
            max_evidence_items=max_evidence_items,
            per_file_count=per_file_count,
            max_evidence_per_file=max_evidence_per_file,
        )
        if omit_reason is not None:
            omitted.append(_replace_status(audit, status="omitted", reason=omit_reason))
            continue

        selected.append(audit)
        selected_index[evidence_id] = evidence
        selected_ids.add(evidence_id)
        per_file_counts[path] = per_file_count + 1
        used_tokens = projected

    for required_id in _required_risk_evidence_ids(package):
        if required_id not in selected_ids and required_id in package.evidence_index:
            warnings.append(f"required_risk_evidence_omitted:{required_id}")

    evidence_payload = {
        evidence_id: evidence.to_dict()
        for evidence_id, evidence in selected_index.items()
    }
    estimated_tokens = estimate_tokens({**base_payload, "evidence_index": evidence_payload})
    context_budget = _context_budget_summary(
        selected=selected,
        omitted=omitted,
        warnings=warnings,
        max_input_tokens=max_input_tokens,
        estimated_tokens=estimated_tokens,
        selected_risk_signal_count=len(package.risk_signals),
        shard_count=shard_count,
        shard_id=shard_id,
        shard_index=shard_index,
        is_refill=is_refill,
    )
    reviewer_context = ReviewerContext(
        schema=LIVE_REVIEW_INPUT_SCHEMA,
        selection_strategy=(
            REFILL_STRATEGY if is_refill else SELECTION_STRATEGY
        ),
        repo_root=str(base_payload["repo_root"]),
        shard_id=shard_id,
        shard_index=shard_index,
        shard_count=shard_count,
        changed_files=list(base_payload["changed_files"]),
        omitted_changed_file_count=int(base_payload["omitted_changed_file_count"]),
        changed_entities=list(base_payload["changed_entities"]),
        risk_signals=list(base_payload["risk_signals"]),
        evidence_index=evidence_payload,
        context_budget=context_budget,
        is_refill=is_refill,
        parent_shard_id=parent_shard_id,
        request_types=list(request_types or []),
    )
    payload = reviewer_context.to_dict()
    return LiveReviewInput(
        payload=payload,
        context_budget=context_budget,
        reviewer_context=reviewer_context,
        selected_evidence=selected,
        omitted_evidence=omitted,
    )


def build_reviewer_contexts(
    package: EvidencePackage,
    *,
    max_input_tokens: int = DEFAULT_CONTEXT_BUDGET_TOKENS,
    max_files: int = DEFAULT_MAX_FILES_PER_AGENT_CALL,
    max_evidence_per_file: int = DEFAULT_MAX_EVIDENCE_PER_FILE,
    max_evidence_items: int = DEFAULT_MAX_EVIDENCE_ITEMS,
) -> list[ReviewerContext]:
    """Build one or more reviewer contexts from a full EvidencePackage."""

    primary = build_live_review_input(
        package,
        max_input_tokens=max_input_tokens,
        max_files=max_files,
        max_evidence_per_file=max_evidence_per_file,
        max_evidence_items=max_evidence_items,
    )
    paths = _changed_paths(package)
    if not primary.context_budget["context_truncated"] and len(paths) <= max(1, max_files):
        return [primary.reviewer_context]

    chunks = [
        paths[index : index + max(1, max_files)]
        for index in range(0, len(paths), max(1, max_files))
    ]
    contexts: list[ReviewerContext] = []
    for index, chunk in enumerate(chunks):
        item = build_live_review_input(
            package,
            max_input_tokens=max_input_tokens,
            max_files=max_files,
            max_evidence_per_file=max_evidence_per_file,
            max_evidence_items=max_evidence_items,
            allowed_paths=set(chunk),
            shard_id=f"shard-{index + 1:03d}",
            shard_index=index,
            shard_count=len(chunks),
        )
        contexts.append(item.reviewer_context)
    return contexts


def build_context_refill(
    package: EvidencePackage,
    parent: ReviewerContext,
    requests: list[ContextRequest],
    *,
    max_input_tokens: int = DEFAULT_CONTEXT_BUDGET_TOKENS,
    max_evidence_per_file: int = DEFAULT_MAX_EVIDENCE_PER_FILE,
    max_context_requests: int = 8,
) -> ReviewerContext | None:
    """Build a one-shot refill context for bounded model requests."""

    selected_ids = set(parent.evidence_index)
    request_slice = [
        request
        for request in requests[: max(0, max_context_requests)]
        if request.request_type in ALLOWED_CONTEXT_REQUEST_TYPES
    ]
    evidence_ids = _requested_evidence_ids(package, selected_ids, request_slice)
    if not evidence_ids:
        return None

    paths = {
        path
        for evidence_id in evidence_ids
        for path in [_path_for_evidence(evidence_id, package.evidence_index.get(evidence_id))]
        if path is not None
    }
    refill = build_live_review_input(
        package,
        max_input_tokens=max_input_tokens,
        max_files=max(1, len(paths) or 1),
        max_evidence_per_file=max_evidence_per_file,
        max_evidence_items=len(evidence_ids),
        allowed_paths=paths or None,
        forced_evidence_ids=evidence_ids,
        shard_id=f"{parent.shard_id}-refill",
        shard_index=parent.shard_index,
        shard_count=parent.shard_count,
        is_refill=True,
        parent_shard_id=parent.shard_id,
        request_types=sorted({request.request_type for request in request_slice}),
    )
    fulfilled_ids = set(refill.reviewer_context.evidence_index)
    for request in request_slice:
        request.fulfilled_evidence_ids = sorted(
            evidence_id for evidence_id in evidence_ids if evidence_id in fulfilled_ids
        )
    return refill.reviewer_context


def aggregate_context_budget(
    contexts: list[ReviewerContext],
    *,
    context_requests: list[ContextRequest] | None = None,
) -> dict[str, Any]:
    """Aggregate per-shard context budget summaries for the final report."""

    if not contexts:
        return context_budget_disabled_summary()
    selected_ids: list[str] = []
    omitted_ids: list[str] = []
    warnings: list[str] = []
    shards: list[dict[str, Any]] = []
    estimated_tokens = 0
    max_tokens = 0
    for context in contexts:
        budget = context.context_budget
        selected = [str(item) for item in budget.get("selected_evidence_ids", [])]
        omitted = [str(item) for item in budget.get("omitted_evidence_ids", [])]
        selected_ids.extend(selected)
        omitted_ids.extend(omitted)
        warnings.extend(str(item) for item in budget.get("warnings", []))
        estimated_tokens += int(budget.get("estimated_input_tokens", 0))
        max_tokens = max(max_tokens, int(budget.get("max_input_tokens", 0)))
        shards.append(
            {
                "shard_id": context.shard_id,
                "shard_index": context.shard_index,
                "is_refill": context.is_refill,
                "parent_shard_id": context.parent_shard_id,
                "selected_evidence_count": len(selected),
                "omitted_evidence_count": len(omitted),
                "estimated_input_tokens": int(
                    budget.get("estimated_input_tokens", 0)
                ),
                "context_truncated": bool(budget.get("context_truncated", False)),
            }
        )

    selected_unique = list(dict.fromkeys(selected_ids))
    omitted_unique = [
        evidence_id
        for evidence_id in dict.fromkeys(omitted_ids)
        if evidence_id not in set(selected_unique)
    ]
    requests = context_requests or []
    return {
        "enabled": True,
        "strategy": SHARDING_STRATEGY if len(contexts) > 1 else SELECTION_STRATEGY,
        "max_input_tokens": max_tokens,
        "estimated_input_tokens": estimated_tokens,
        "selected_evidence_count": len(selected_unique),
        "omitted_evidence_count": len(omitted_unique),
        "selected_evidence_ids": selected_unique,
        "omitted_evidence_ids": omitted_unique[:200],
        "selected_risk_signal_count": sum(
            len(context.risk_signals) for context in contexts if not context.is_refill
        ),
        "context_truncated": bool(omitted_unique)
        or any(shard["context_truncated"] for shard in shards),
        "shard_count": len([context for context in contexts if not context.is_refill]),
        "refill_count": len([context for context in contexts if context.is_refill]),
        "context_request_count": len(requests),
        "context_requests": [request.to_dict() for request in requests],
        "shards": shards,
        "warnings": list(dict.fromkeys(warnings)),
    }


def context_budget_disabled_summary() -> dict[str, Any]:
    """Return a stable disabled context-budget report."""

    return {
        "enabled": False,
        "strategy": SELECTION_STRATEGY,
        "max_input_tokens": 0,
        "estimated_input_tokens": 0,
        "selected_evidence_count": 0,
        "omitted_evidence_count": 0,
        "selected_evidence_ids": [],
        "omitted_evidence_ids": [],
        "selected_risk_signal_count": 0,
        "context_truncated": False,
        "shard_count": 0,
        "refill_count": 0,
        "context_request_count": 0,
        "context_requests": [],
        "shards": [],
        "warnings": [],
    }


def _ranked_candidate_ids(
    package: EvidencePackage,
    *,
    allowed_paths: set[str] | None = None,
    forced_evidence_ids: set[str] | None = None,
) -> list[str]:
    if forced_evidence_ids is not None:
        candidate_ids = {
            evidence_id
            for evidence_id in forced_evidence_ids
            if evidence_id in package.evidence_index
        }
    else:
        candidate_ids = set(package.evidence_index)
    for signal in package.risk_signals:
        candidate_ids.update(
            evidence_id
            for evidence_id in signal.evidence_ids
            if evidence_id in package.evidence_index
        )
    if allowed_paths is not None:
        candidate_ids = {
            evidence_id
            for evidence_id in candidate_ids
            if _path_for_evidence(
                evidence_id, package.evidence_index.get(evidence_id)
            )
            in allowed_paths
        }
    return sorted(candidate_ids, key=lambda item: (-score_evidence(package, item), item))


def _base_payload(
    package: EvidencePackage,
    *,
    max_files: int,
    allowed_paths: set[str] | None = None,
) -> dict[str, Any]:
    changed_file_summaries = _changed_file_summaries(package, allowed_paths=allowed_paths)
    changed_files = changed_file_summaries[:max_files]
    return {
        "schema": LIVE_REVIEW_INPUT_SCHEMA,
        "selection_strategy": SELECTION_STRATEGY,
        "repo_root": package.repo_root,
        "changed_files": changed_files,
        "omitted_changed_file_count": max(
            0, len(changed_file_summaries) - len(changed_files)
        ),
        "changed_entities": [
            entity.to_dict()
            for entity in _changed_entities(package, allowed_paths=allowed_paths)[
                :DEFAULT_MAX_EVIDENCE_ITEMS
            ]
        ],
        "risk_signals": [
            _risk_card(package, signal)
            for signal in sorted(
                _risk_signals(package, allowed_paths=allowed_paths),
                key=_risk_sort_key,
            )
        ],
    }


def _changed_file_summaries(
    package: EvidencePackage,
    *,
    allowed_paths: set[str] | None = None,
) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for change in package.changed_files:
        path = change.new_path or change.old_path
        if allowed_paths is not None and path not in allowed_paths:
            continue
        summaries.append(
            {
                "old_path": change.old_path,
                "new_path": change.new_path,
                "change_type": change.change_type,
                "hunk_count": len(change.hunks),
                "changed_line_count": sum(
                    1
                    for hunk in change.hunks
                    for line in hunk.lines
                    if line.line_type in {"added", "removed"}
                ),
                "first_diff_evidence_id": _first_diff_evidence_id(package, path),
            }
        )
    return summaries


def _changed_entities(
    package: EvidencePackage,
    *,
    allowed_paths: set[str] | None,
):
    if allowed_paths is None:
        return package.changed_entities
    return [entity for entity in package.changed_entities if entity.path in allowed_paths]


def _risk_signals(
    package: EvidencePackage,
    *,
    allowed_paths: set[str] | None,
) -> list[RiskSignal]:
    if allowed_paths is None:
        return list(package.risk_signals)
    signals: list[RiskSignal] = []
    for signal in package.risk_signals:
        evidence_paths = {
            _path_for_evidence(
                evidence_id, package.evidence_index.get(evidence_id)
            )
            for evidence_id in signal.evidence_ids
        }
        evidence_paths.add(_path_for_evidence(_risk_evidence_id(signal), None))
        if evidence_paths & allowed_paths:
            signals.append(signal)
    return signals


def _risk_card(
    package: EvidencePackage,
    signal: RiskSignal,
    *,
    max_evidence_ids: int = DEFAULT_MAX_RISK_EVIDENCE_IDS,
) -> dict[str, Any]:
    evidence_ids = [
        evidence_id
        for evidence_id in signal.evidence_ids
        if evidence_id in package.evidence_index
    ]
    risk_id = _risk_evidence_id(signal)
    if risk_id in package.evidence_index:
        evidence_ids.insert(0, risk_id)
    deduped = list(dict.fromkeys(evidence_ids))
    selected = deduped[: max(1, max_evidence_ids)]
    return {
        "tag": signal.tag,
        "confidence": signal.confidence,
        "reason": signal.reason,
        "primary_evidence_ids": selected,
        "omitted_evidence_id_count": max(0, len(deduped) - len(selected)),
    }


def _changed_paths(package: EvidencePackage) -> list[str]:
    paths: list[str] = []
    for change in package.changed_files:
        path = change.new_path or change.old_path
        if path is not None and path not in paths:
            paths.append(path)
    return paths


def _required_risk_evidence_ids(package: EvidencePackage) -> list[str]:
    ids: list[str] = []
    for signal in sorted(package.risk_signals, key=_risk_sort_key):
        for evidence_id in signal.evidence_ids:
            if evidence_id in package.evidence_index:
                ids.append(evidence_id)
                break
    return ids


def _first_diff_evidence_id(
    package: EvidencePackage,
    path: str | None,
) -> str | None:
    if path is None:
        return None
    for evidence_id, evidence in package.evidence_index.items():
        if evidence.kind == "diff" and _path_for_evidence(evidence_id, evidence) == path:
            return evidence_id
    return None


def _risk_sort_key(signal: RiskSignal) -> tuple[float, str]:
    return (-_HIGH_RISK_SCORE.get(signal.tag, 35.0), signal.tag)


def _audit_entry(
    package: EvidencePackage,
    evidence_id: str,
    *,
    status: str,
    reason: str,
) -> SelectedEvidenceAudit:
    evidence = package.evidence_index[evidence_id]
    return SelectedEvidenceAudit(
        evidence_id=evidence_id,
        status=status,
        score=score_evidence(package, evidence_id),
        reason=reason,
        estimated_tokens=estimate_tokens(evidence.to_dict()),
        source=evidence.source,
    )


def _replace_status(
    item: SelectedEvidenceAudit,
    *,
    status: str,
    reason: str,
) -> SelectedEvidenceAudit:
    return SelectedEvidenceAudit(
        evidence_id=item.evidence_id,
        status=status,
        score=item.score,
        reason=reason,
        estimated_tokens=item.estimated_tokens,
        source=item.source,
    )


def _selection_reason(package: EvidencePackage, evidence_id: str) -> str:
    if evidence_id.startswith("risk:"):
        return "risk_summary"
    if any(evidence_id in signal.evidence_ids for signal in package.risk_signals):
        return "risk_linked"
    if evidence_id.startswith("diff:"):
        return "changed_diff"
    if evidence_id.startswith("entity:"):
        return "changed_entity"
    return "ranked_context"


def _omit_reason(
    *,
    projected: int,
    max_input_tokens: int,
    selected_count: int,
    max_evidence_items: int,
    per_file_count: int,
    max_evidence_per_file: int,
) -> str | None:
    if projected > max_input_tokens:
        return "over_budget"
    if selected_count >= max_evidence_items:
        return "evidence_limit_reached"
    if per_file_count >= max_evidence_per_file:
        return "file_limit_reached"
    return None


def _context_budget_summary(
    *,
    selected: list[SelectedEvidenceAudit],
    omitted: list[SelectedEvidenceAudit],
    warnings: list[str],
    max_input_tokens: int,
    estimated_tokens: int,
    selected_risk_signal_count: int,
    shard_count: int,
    shard_id: str,
    shard_index: int,
    is_refill: bool,
) -> dict[str, Any]:
    selected_ids = [item.evidence_id for item in selected]
    omitted_ids = [item.evidence_id for item in omitted]
    return {
        "enabled": True,
        "strategy": SELECTION_STRATEGY,
        "max_input_tokens": max_input_tokens,
        "estimated_input_tokens": estimated_tokens,
        "selected_evidence_count": len(selected_ids),
        "omitted_evidence_count": len(omitted_ids),
        "selected_evidence_ids": selected_ids,
        "omitted_evidence_ids": omitted_ids[:200],
        "selected_risk_signal_count": selected_risk_signal_count,
        "context_truncated": bool(omitted_ids) or estimated_tokens > max_input_tokens,
        "shard_count": shard_count,
        "shard_id": shard_id,
        "shard_index": shard_index,
        "is_refill": is_refill,
        "warnings": list(warnings),
    }


def _requested_evidence_ids(
    package: EvidencePackage,
    selected_ids: set[str],
    requests: list[ContextRequest],
) -> set[str]:
    requested: set[str] = set()
    for context_request in requests:
        explicit_ids = [
            evidence_id
            for evidence_id in context_request.evidence_ids
            if evidence_id in package.evidence_index
        ]
        requested.update(explicit_ids)
        if context_request.request_type == "same_file_more_evidence":
            if context_request.path is not None:
                requested.update(_evidence_ids_for_path(package, context_request.path))
        elif context_request.request_type == "related_tests":
            requested.update(_test_evidence_ids(package, context_request.path))
        elif context_request.request_type == "related_symbol":
            requested.update(_entity_evidence_ids(package, context_request.path))
        elif context_request.request_type == "risk_evidence":
            requested.update(_risk_related_evidence_ids(package, context_request))
    return {
        evidence_id
        for evidence_id in requested
        if evidence_id in package.evidence_index and evidence_id not in selected_ids
    }


def _evidence_ids_for_path(package: EvidencePackage, path: str) -> set[str]:
    return {
        evidence_id
        for evidence_id, evidence in package.evidence_index.items()
        if _path_for_evidence(evidence_id, evidence) == path
    }


def _test_evidence_ids(package: EvidencePackage, path: str | None) -> set[str]:
    ids: set[str] = set()
    for evidence_id, evidence in package.evidence_index.items():
        if evidence.kind != "test_discovery":
            continue
        if path is None or path in evidence.message or path == evidence.source:
            ids.add(evidence_id)
    return ids


def _entity_evidence_ids(package: EvidencePackage, path: str | None) -> set[str]:
    return {
        evidence_id
        for evidence_id, evidence in package.evidence_index.items()
        if evidence.kind == "entity"
        and (path is None or _path_for_evidence(evidence_id, evidence) == path)
    }


def _risk_related_evidence_ids(
    package: EvidencePackage,
    context_request: ContextRequest,
) -> set[str]:
    ids: set[str] = set()
    for signal in package.risk_signals:
        if context_request.risk_tag is not None and signal.tag != context_request.risk_tag:
            continue
        if context_request.path is not None:
            signal_paths = {
                _path_for_evidence(
                    evidence_id, package.evidence_index.get(evidence_id)
                )
                for evidence_id in signal.evidence_ids
            }
            signal_paths.add(_path_for_evidence(_risk_evidence_id(signal), None))
            if context_request.path not in signal_paths:
                continue
        ids.update(
            evidence_id
            for evidence_id in signal.evidence_ids
            if evidence_id in package.evidence_index
        )
        risk_id = _risk_evidence_id(signal)
        if risk_id in package.evidence_index:
            ids.add(risk_id)
    return ids


def _risk_evidence_id(signal: RiskSignal) -> str:
    path = _signal_path(signal)
    return f"risk:{signal.tag}:{path}" if path else f"risk:{signal.tag}:patch"


def _signal_path(signal: RiskSignal) -> str | None:
    for evidence_id in signal.evidence_ids:
        path = _evidence_path(evidence_id)
        if path is not None:
            return path
    return None


def _path_for_evidence(
    evidence_id: str,
    evidence: ReviewEvidence | None,
) -> str | None:
    path = _evidence_path(evidence_id)
    if path is not None:
        return path
    if evidence is None:
        return None
    if ":" in evidence.source:
        return evidence.source.rsplit(":", 1)[0]
    return evidence.source


def _evidence_path(evidence_id: str) -> str | None:
    parts = evidence_id.split(":")
    if len(parts) >= 3 and parts[0] == "diff":
        return ":".join(parts[1:-1])
    if len(parts) >= 3 and parts[0] == "entity":
        return parts[1]
    if len(parts) >= 3 and parts[0] == "risk":
        return ":".join(parts[2:])
    if len(parts) >= 2 and parts[0] in {"test_discovery", "hygiene"}:
        return parts[1]
    return None
