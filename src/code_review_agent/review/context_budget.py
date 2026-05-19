"""Budget and selection helpers for live review inputs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from code_review_agent.models import (
    ContextRequest,
    EvidencePackage,
    ReviewEvidence,
    ReviewerContext,
    RiskSignal,
)
from code_review_agent.review.schema import EvidenceStore


DEFAULT_CONTEXT_BUDGET_TOKENS = 24000
DEFAULT_MAX_SHARD_INPUT_TOKENS = 9000
DEFAULT_MAX_FILES_PER_AGENT_CALL = 8
DEFAULT_MAX_EVIDENCE_PER_FILE = 80
DEFAULT_MAX_EVIDENCE_ITEMS = 400
DEFAULT_MAX_RISK_EVIDENCE_IDS = 5
DEFAULT_PRIMARY_EVIDENCE_PER_RISK = 4
DEFAULT_MAX_CHANGED_ENTITY_CARDS = 24
DEFAULT_MAX_RISK_CARDS = 24
DEFAULT_MANIFEST_EVIDENCE_ID_LIMIT = 40
DEFAULT_MANIFEST_PATH_LIMIT = 30
DEFAULT_MANIFEST_PATH_SAMPLE_LIMIT = 4
DEFAULT_MANIFEST_RISK_LIMIT = 24
DEFAULT_MAX_REFILL_EVIDENCE_PER_REQUEST = 8
DEFAULT_MAX_REVIEW_GUIDELINES = 12
DEFAULT_MAX_REVIEW_GUIDELINE_CHARS = 700
DEFAULT_GUIDELINE_MATCHED_TERM_LIMIT = 10
LIVE_REVIEW_INPUT_SCHEMA = "live_review_input_v1"
SELECTION_STRATEGY = "risk_first_v1"
SHARDING_STRATEGY = "file_risk_shards_v1"
REFILL_STRATEGY = "one_shot_refill_v1"
COMPACT_CONTEXT_PROFILE = "risk_compact_manifest_v1"
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
    "diff_hunk": 62.0,
    "risk": 55.0,
    "diff": 35.0,
    "entity": 40.0,
    "test_discovery": 25.0,
    "hygiene": 15.0,
}
_DEFAULT_EXPANDED_EVIDENCE_KINDS = frozenset(
    {"diff_hunk", "test_discovery", "hygiene"}
)


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

    if evidence_id.startswith(("diff:", "diff_hunk:")):
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
    omitted_by_id: dict[str, SelectedEvidenceAudit] = {}
    selected_index: dict[str, ReviewEvidence] = {}
    selected_ids: set[str] = set()
    per_file_counts: dict[str, int] = {}
    warnings: list[str] = []

    base_payload = _base_payload(package, max_files=max_files, allowed_paths=allowed_paths)
    used_tokens = estimate_tokens(base_payload)
    available_ids = _available_evidence_ids(
        package,
        allowed_paths=allowed_paths,
        forced_evidence_ids=forced_evidence_ids,
    )
    candidate_ids = _expanded_candidate_ids(
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
            omitted_by_id[evidence_id] = _replace_status(
                audit, status="omitted", reason=omit_reason
            )
            continue

        selected.append(audit)
        selected_index[evidence_id] = evidence
        selected_ids.add(evidence_id)
        per_file_counts[path] = per_file_count + 1
        used_tokens = projected

    for evidence_id in available_ids:
        if evidence_id in selected_ids or evidence_id in omitted_by_id:
            continue
        omitted_by_id[evidence_id] = _audit_entry(
            package,
            evidence_id,
            status="omitted",
            reason="manifest_only",
        )

    omitted = sorted(
        omitted_by_id.values(),
        key=lambda item: (-item.score, item.evidence_id),
    )

    for required_id in _required_risk_evidence_ids(
        package,
        allowed_paths=allowed_paths,
    ):
        if (
            required_id in package.evidence_index
            and not _required_evidence_satisfied(package, required_id, selected_ids)
        ):
            warnings.append(f"required_risk_evidence_omitted:{required_id}")

    evidence_payload = {
        evidence_id: evidence.to_dict()
        for evidence_id, evidence in selected_index.items()
    }
    available_context = _available_context_manifest(
        package,
        available_ids=available_ids,
        selected_ids=selected_ids,
        allowed_paths=allowed_paths,
    )
    estimated_tokens = estimate_tokens(
        {
            **base_payload,
            "evidence_index": evidence_payload,
            "available_context": available_context,
        }
    )
    context_budget = _context_budget_summary(
        selected=selected,
        omitted=omitted,
        warnings=warnings,
        max_input_tokens=max_input_tokens,
        estimated_tokens=estimated_tokens,
        selected_risk_signal_count=len(base_payload["risk_signals"]),
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
        review_guidelines=list(base_payload.get("review_guidelines", [])),
        evidence_index=evidence_payload,
        available_context=available_context,
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

    shard_input_tokens = min(
        max(1, max_input_tokens),
        DEFAULT_MAX_SHARD_INPUT_TOKENS,
    )
    primary = build_live_review_input(
        package,
        max_input_tokens=shard_input_tokens,
        max_files=max_files,
        max_evidence_per_file=max_evidence_per_file,
        max_evidence_items=max_evidence_items,
    )
    paths = _changed_paths(package)
    if not primary.context_budget["context_truncated"] and len(paths) <= max(1, max_files):
        return [primary.reviewer_context]

    chunks = _path_chunks_by_budget(
        package,
        paths,
        max_input_tokens=shard_input_tokens,
        max_files=max_files,
        max_evidence_per_file=max_evidence_per_file,
        max_evidence_items=max_evidence_items,
    )
    contexts: list[ReviewerContext] = []
    for index, chunk in enumerate(chunks):
        item = build_live_review_input(
            package,
            max_input_tokens=shard_input_tokens,
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
    max_evidence_per_request: int = DEFAULT_MAX_REFILL_EVIDENCE_PER_REQUEST,
) -> ReviewerContext | None:
    """Build a one-shot refill context for bounded model requests."""

    refill_input_tokens = min(
        max(1, max_input_tokens),
        DEFAULT_MAX_SHARD_INPUT_TOKENS,
    )
    selected_ids = set(parent.evidence_index)
    request_slice = [
        request
        for request in requests
        if request.request_type in ALLOWED_CONTEXT_REQUEST_TYPES
    ][: max(0, max_context_requests)]
    evidence_by_request = _requested_evidence_ids_by_request(
        package,
        selected_ids,
        request_slice,
        max_evidence_per_request=max_evidence_per_request,
    )
    evidence_ids = {
        evidence_id
        for ids in evidence_by_request.values()
        for evidence_id in ids
    }
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
        max_input_tokens=refill_input_tokens,
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
        requested_ids = evidence_by_request.get(id(request), [])
        request.fulfilled_evidence_ids = sorted(
            evidence_id
            for evidence_id in requested_ids
            if evidence_id in fulfilled_ids
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
    selected_unique_set = set(selected_unique)
    omitted_unique = [
        evidence_id
        for evidence_id in dict.fromkeys(omitted_ids)
        if evidence_id not in selected_unique_set
    ]
    requests = context_requests or []
    return {
        "enabled": True,
        "strategy": SHARDING_STRATEGY if len(contexts) > 1 else SELECTION_STRATEGY,
        "context_profile": COMPACT_CONTEXT_PROFILE,
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
        "warnings": _unresolved_context_warnings(warnings, selected_unique_set),
    }


def context_budget_disabled_summary() -> dict[str, Any]:
    """Return a stable disabled context-budget report."""

    return {
        "enabled": False,
        "strategy": SELECTION_STRATEGY,
        "context_profile": COMPACT_CONTEXT_PROFILE,
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


def _unresolved_context_warnings(
    warnings: list[str],
    selected_ids: set[str],
) -> list[str]:
    unresolved: list[str] = []
    prefix = "required_risk_evidence_omitted:"
    for warning in dict.fromkeys(warnings):
        if warning.startswith(prefix) and warning.removeprefix(prefix) in selected_ids:
            continue
        unresolved.append(warning)
    return unresolved


def _path_chunks_by_budget(
    package: EvidencePackage,
    paths: list[str],
    *,
    max_input_tokens: int,
    max_files: int,
    max_evidence_per_file: int,
    max_evidence_items: int,
) -> list[list[str]]:
    chunks: list[list[str]] = []
    current: list[str] = []
    max_files = max(1, max_files)
    for path in paths:
        candidate = [*current, path]
        if current and len(candidate) > max_files:
            chunks.append(current)
            current = [path]
            continue
        if current and _candidate_exceeds_shard_budget(
            package,
            candidate,
            max_input_tokens=max_input_tokens,
            max_files=max_files,
            max_evidence_per_file=max_evidence_per_file,
            max_evidence_items=max_evidence_items,
        ):
            chunks.append(current)
            current = [path]
            continue
        current = candidate
    if current:
        chunks.append(current)
    return chunks or [[]]


def _candidate_exceeds_shard_budget(
    package: EvidencePackage,
    paths: list[str],
    *,
    max_input_tokens: int,
    max_files: int,
    max_evidence_per_file: int,
    max_evidence_items: int,
) -> bool:
    candidate = build_live_review_input(
        package,
        max_input_tokens=max_input_tokens,
        max_files=max_files,
        max_evidence_per_file=max_evidence_per_file,
        max_evidence_items=max_evidence_items,
        allowed_paths=set(paths),
    )
    return int(candidate.context_budget["estimated_input_tokens"]) > max_input_tokens


def _available_evidence_ids(
    package: EvidencePackage,
    *,
    allowed_paths: set[str] | None = None,
    forced_evidence_ids: set[str] | None = None,
) -> list[str]:
    store = EvidenceStore.from_legacy_package(package)
    if forced_evidence_ids is not None:
        candidate_ids = {
            evidence_id
            for evidence_id in forced_evidence_ids
            if store.get(evidence_id) is not None
        }
    else:
        candidate_ids = set(store.items)
    if allowed_paths is not None:
        candidate_ids = {
            evidence_id
            for evidence_id in candidate_ids
            if _store_item_path(store, evidence_id) in allowed_paths
        }
    return sorted(candidate_ids, key=lambda item: (-score_evidence(package, item), item))


def _expanded_candidate_ids(
    package: EvidencePackage,
    *,
    allowed_paths: set[str] | None = None,
    forced_evidence_ids: set[str] | None = None,
) -> list[str]:
    if forced_evidence_ids is not None:
        return _available_evidence_ids(
            package,
            allowed_paths=allowed_paths,
            forced_evidence_ids=forced_evidence_ids,
        )

    candidate_ids: list[str] = []
    for signal in sorted(
        _risk_signals(package, allowed_paths=allowed_paths),
        key=_risk_sort_key,
    ):
        candidate_ids.extend(
            _primary_evidence_ids_for_signal(
                package,
                signal,
                max_evidence_ids=DEFAULT_PRIMARY_EVIDENCE_PER_RISK,
                expanded_only=True,
                allowed_paths=allowed_paths,
            )
        )

    for change in package.changed_files:
        path = change.new_path or change.old_path
        if path is None or (allowed_paths is not None and path not in allowed_paths):
            continue
        candidate_ids.extend(_hunk_evidence_ids_for_change(package, change))

    deduped = [
        evidence_id
        for evidence_id in dict.fromkeys(candidate_ids)
        if evidence_id in package.evidence_index
    ]
    return sorted(deduped, key=lambda item: (-score_evidence(package, item), item))


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
        "context_profile": COMPACT_CONTEXT_PROFILE,
        "repo_root": package.repo_root,
        "changed_files": changed_files,
        "omitted_changed_file_count": max(
            0, len(changed_file_summaries) - len(changed_files)
        ),
        "changed_entities": [
            entity.to_dict()
            for entity in _changed_entities(package, allowed_paths=allowed_paths)[
                :DEFAULT_MAX_CHANGED_ENTITY_CARDS
            ]
        ],
        "risk_signals": [
            _risk_card(package, signal, allowed_paths=allowed_paths)
            for signal in sorted(
                _risk_signals(package, allowed_paths=allowed_paths),
                key=_risk_sort_key,
            )[:DEFAULT_MAX_RISK_CARDS]
        ],
        "review_guidelines": _review_guidelines(package, allowed_paths=allowed_paths),
    }


def _review_guidelines(
    package: EvidencePackage,
    *,
    allowed_paths: set[str] | None,
) -> list[dict[str, Any]]:
    raw_guidelines = package.metadata.get("review_guidelines", [])
    if not isinstance(raw_guidelines, list):
        return []
    cards: list[dict[str, Any]] = []
    for index, item in enumerate(raw_guidelines):
        if isinstance(item, str):
            guideline = {"title": f"Guideline {index + 1}", "body": item}
        elif isinstance(item, dict):
            guideline = dict(item)
        else:
            continue
        title = str(guideline.get("title") or guideline.get("name") or f"Guideline {index + 1}")
        body_parts = [
            str(guideline.get("objective") or ""),
            str(guideline.get("success_criteria") or ""),
            str(guideline.get("failure_criteria") or ""),
            str(guideline.get("description") or ""),
            str(guideline.get("body") or ""),
        ]
        body = " ".join(part.strip() for part in body_parts if part.strip())
        if len(body) > DEFAULT_MAX_REVIEW_GUIDELINE_CHARS:
            body = f"{body[:DEFAULT_MAX_REVIEW_GUIDELINE_CHARS - 3]}..."
        cards.append({"title": title[:180], "body": body})
    return _rank_review_guidelines(package, cards, allowed_paths=allowed_paths)


def _rank_review_guidelines(
    package: EvidencePackage,
    guidelines: list[dict[str, Any]],
    *,
    allowed_paths: set[str] | None,
) -> list[dict[str, Any]]:
    if not guidelines:
        return []

    shard_text = _guideline_retrieval_text(package, allowed_paths=allowed_paths)
    changed_paths = set(allowed_paths or _changed_paths(package))
    scored: list[tuple[float, int, dict[str, Any]]] = []
    for index, guideline in enumerate(guidelines):
        score, matched_terms = _score_review_guideline(
            guideline,
            changed_paths=changed_paths,
            shard_text=shard_text,
        )
        if score <= 0:
            continue
        ranked = dict(guideline)
        ranked["selection_score"] = round(score, 3)
        ranked["matched_terms"] = matched_terms[:DEFAULT_GUIDELINE_MATCHED_TERM_LIMIT]
        scored.append((score, index, ranked))

    if not scored:
        return []
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in scored[:DEFAULT_MAX_REVIEW_GUIDELINES]]


def _score_review_guideline(
    guideline: dict[str, Any],
    *,
    changed_paths: set[str],
    shard_text: str,
) -> tuple[float, list[str]]:
    guideline_text = f"{guideline.get('title', '')} {guideline.get('body', '')}"
    guideline_tokens = _keyword_tokens(guideline_text)
    shard_tokens = _keyword_tokens(shard_text)
    matched_terms = sorted(guideline_tokens & shard_tokens)
    score = float(len(matched_terms))

    lower_guideline = guideline_text.lower()
    lower_shard = shard_text.lower()
    for path in changed_paths:
        normalized = path.replace("\\", "/").lower()
        path_parts = [part for part in re.split(r"[/_.-]+", normalized) if part]
        file_name = path_parts[-1] if path_parts else normalized
        suffix = normalized.rsplit(".", 1)[-1] if "." in normalized else ""
        if normalized and normalized in lower_guideline:
            score += 30.0
            matched_terms.append(path)
        if file_name and file_name in lower_guideline:
            score += 8.0
            matched_terms.append(file_name)
        if suffix and suffix in _extension_terms(lower_guideline):
            score += 4.0
            matched_terms.append(f".{suffix}")
        for part in path_parts[:-1]:
            if len(part) >= 4 and part in lower_guideline:
                score += 3.0
                matched_terms.append(part)

    for phrase in _quoted_or_code_phrases(lower_guideline):
        if len(phrase) >= 3 and phrase in lower_shard:
            score += 12.0
            matched_terms.append(phrase)

    return score, list(dict.fromkeys(matched_terms))


def _guideline_retrieval_text(
    package: EvidencePackage,
    *,
    allowed_paths: set[str] | None,
) -> str:
    parts: list[str] = []
    for change in package.changed_files:
        path = change.new_path or change.old_path
        if path is None or (allowed_paths is not None and path not in allowed_paths):
            continue
        parts.extend([path, change.change_type, _file_role(path)])
        for hunk in change.hunks:
            parts.append(hunk.section_header)
            parts.extend(line.content for line in hunk.lines)
    for entity in _changed_entities(package, allowed_paths=allowed_paths):
        parts.extend([entity.path, entity.name, entity.entity_type])
    for signal in _risk_signals(package, allowed_paths=allowed_paths):
        parts.extend([signal.tag, signal.reason])
    return "\n".join(part for part in parts if part)


def _keyword_tokens(text: str) -> set[str]:
    tokens = {
        token.lower()
        for token in re.findall(r"[A-Za-z_][A-Za-z0-9_@.-]{2,}", text)
    }
    stop_words = {
        "all",
        "and",
        "are",
        "code",
        "contain",
        "contains",
        "criteria",
        "ensure",
        "file",
        "files",
        "for",
        "from",
        "must",
        "not",
        "the",
        "this",
        "use",
        "uses",
        "using",
        "with",
    }
    return {token for token in tokens if token not in stop_words}


def _extension_terms(text: str) -> set[str]:
    terms: set[str] = set(re.findall(r"\.([a-z0-9]{1,6})\b", text))
    language_extensions = {
        "javascript": "js",
        "typescript": "ts",
        "python": "py",
        "csharp": "cs",
        "react": "tsx",
        "markdown": "md",
        "yaml": "yml",
    }
    for language, suffix in language_extensions.items():
        if language in text:
            terms.add(suffix)
    return terms


def _quoted_or_code_phrases(text: str) -> list[str]:
    phrases = re.findall(r"`([^`]+)`|'([^']+)'|\"([^\"]+)\"", text)
    flattened = [part for match in phrases for part in match if part]
    return [
        phrase.strip().lower()
        for phrase in flattened
        if phrase.strip() and len(phrase.strip()) <= 80
    ]


def _changed_file_summaries(
    package: EvidencePackage,
    *,
    allowed_paths: set[str] | None = None,
) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for change in package.changed_files:
        path = change.new_path or change.old_path
        if path is None:
            continue
        if allowed_paths is not None and path not in allowed_paths:
            continue
        summaries.append(
            {
                "path": path,
                "old_path": change.old_path,
                "new_path": change.new_path,
                "change_type": change.change_type,
                "file_role": _file_role(path),
                "hunk_count": len(change.hunks),
                "changed_line_count": sum(
                    1
                    for hunk in change.hunks
                    for line in hunk.lines
                    if line.line_type in {"added", "removed"}
                ),
                "first_diff_evidence_id": _first_diff_evidence_id(package, path),
                "available_evidence_count": len(_evidence_ids_for_path(package, path)),
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
    allowed_paths: set[str] | None = None,
) -> dict[str, Any]:
    risk_id = _risk_evidence_id(signal)
    evidence_ids = [
        evidence_id
        for evidence_id in signal.evidence_ids
        if evidence_id in package.evidence_index
    ]
    primary_ids = _primary_evidence_ids_for_signal(
        package,
        signal,
        max_evidence_ids=max_evidence_ids,
        expanded_only=True,
        allowed_paths=allowed_paths,
    )
    deduped = list(dict.fromkeys(evidence_ids))
    return {
        "tag": signal.tag,
        "confidence": signal.confidence,
        "reason": signal.reason,
        "risk_evidence_id": risk_id if risk_id in package.evidence_index else None,
        "primary_evidence_ids": primary_ids,
        "related_evidence_id_count": len(deduped),
        "omitted_evidence_id_count": max(0, len(deduped) - len(primary_ids)),
    }


def _primary_evidence_ids_for_signal(
    package: EvidencePackage,
    signal: RiskSignal,
    *,
    max_evidence_ids: int,
    expanded_only: bool,
    allowed_paths: set[str] | None = None,
) -> list[str]:
    ids: list[str] = []
    for evidence_id in signal.evidence_ids:
        evidence = package.evidence_index.get(evidence_id)
        if evidence is None:
            continue
        if (
            allowed_paths is not None
            and _path_for_evidence(evidence_id, evidence) not in allowed_paths
        ):
            continue
        if expanded_only and evidence.kind == "diff":
            mapped_id = _hunk_evidence_id_for_line(package, evidence_id)
            if mapped_id is None:
                continue
            evidence_id = mapped_id
            evidence = package.evidence_index[evidence_id]
        if expanded_only and evidence.kind not in _DEFAULT_EXPANDED_EVIDENCE_KINDS:
            continue
        ids.append(evidence_id)
        if len(ids) >= max(1, max_evidence_ids):
            break
    return list(dict.fromkeys(ids))


def _available_context_manifest(
    package: EvidencePackage,
    *,
    available_ids: list[str],
    selected_ids: set[str],
    allowed_paths: set[str] | None,
) -> dict[str, Any]:
    omitted_ids = [evidence_id for evidence_id in available_ids if evidence_id not in selected_ids]
    omitted_by_path: dict[str, list[str]] = {}
    for evidence_id in omitted_ids:
        evidence = package.evidence_index.get(evidence_id)
        path = _path_for_evidence(evidence_id, evidence) or "<unknown>"
        omitted_by_path.setdefault(path, []).append(evidence_id)

    paths: list[dict[str, Any]] = []
    for path, evidence_ids in sorted(omitted_by_path.items()):
        kinds = _kind_counts(package, evidence_ids)
        paths.append(
            {
                "path": path,
                "omitted_evidence_count": len(evidence_ids),
                "kinds": kinds,
                "sample_evidence_ids": evidence_ids[:DEFAULT_MANIFEST_PATH_SAMPLE_LIMIT],
                "request_hints": _request_hints_for_kinds(kinds),
            }
        )

    risks: list[dict[str, Any]] = []
    available_set = set(available_ids)
    for signal in sorted(
        _risk_signals(package, allowed_paths=allowed_paths),
        key=_risk_sort_key,
    ):
        related_ids = [
            evidence_id
            for evidence_id in signal.evidence_ids
            if evidence_id in package.evidence_index and evidence_id in available_set
        ]
        omitted_related = [
            evidence_id for evidence_id in related_ids if evidence_id not in selected_ids
        ]
        risks.append(
            {
                "tag": signal.tag,
                "confidence": signal.confidence,
                "path": _path_from_evidence_ids(signal.evidence_ids, package),
                "selected_evidence_ids": [
                    evidence_id for evidence_id in related_ids if evidence_id in selected_ids
                ],
                "omitted_evidence_count": len(omitted_related),
                "sample_omitted_evidence_ids": omitted_related[
                    :DEFAULT_MANIFEST_PATH_SAMPLE_LIMIT
                ],
            }
        )

    return {
        "profile": COMPACT_CONTEXT_PROFILE,
        "request_types": sorted(ALLOWED_CONTEXT_REQUEST_TYPES),
        "available_evidence_count": len(available_ids),
        "selected_evidence_count": len(selected_ids),
        "omitted_evidence_count": len(omitted_ids),
        "omitted_evidence_ids": omitted_ids[:DEFAULT_MANIFEST_EVIDENCE_ID_LIMIT],
        "omitted_evidence_id_limit": DEFAULT_MANIFEST_EVIDENCE_ID_LIMIT,
        "paths": paths[:DEFAULT_MANIFEST_PATH_LIMIT],
        "risks": risks[:DEFAULT_MANIFEST_RISK_LIMIT],
    }


def _kind_counts(package: EvidencePackage, evidence_ids: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for evidence_id in evidence_ids:
        evidence = package.evidence_index.get(evidence_id)
        kind = evidence.kind if evidence is not None else "unknown"
        counts[kind] = counts.get(kind, 0) + 1
    return dict(sorted(counts.items()))


def _request_hints_for_kinds(kinds: dict[str, int]) -> list[str]:
    hints: list[str] = []
    if kinds.get("diff", 0):
        hints.append("same_file_more_evidence")
    if kinds.get("diff_hunk", 0):
        hints.append("same_file_more_evidence")
    if kinds.get("test_discovery", 0):
        hints.append("related_tests")
    if kinds.get("entity", 0):
        hints.append("related_symbol")
    if kinds.get("risk", 0):
        hints.append("risk_evidence")
    return hints


def _file_role(path: str | None) -> str:
    if path is None:
        return "unknown"
    normalized = path.replace("\\", "/")
    name = normalized.rsplit("/", 1)[-1]
    if normalized.startswith("docs/") or name.endswith((".md", ".rst", ".txt")):
        return "docs"
    if "tests/" in f"{normalized}/" or name.startswith("test_") or name.endswith("_test.py"):
        return "test"
    if name in {"pyproject.toml", "setup.py", "setup.cfg"} or normalized.startswith(
        ".github/workflows/"
    ):
        return "config"
    if normalized.startswith("src/"):
        return "source"
    return "other"


def _path_from_evidence_ids(
    evidence_ids: list[str],
    package: EvidencePackage,
) -> str | None:
    for evidence_id in evidence_ids:
        evidence = package.evidence_index.get(evidence_id)
        path = _path_for_evidence(evidence_id, evidence)
        if path is not None:
            return path
    return None


def _changed_paths(package: EvidencePackage) -> list[str]:
    paths: list[str] = []
    for change in package.changed_files:
        path = change.new_path or change.old_path
        if path is not None and path not in paths:
            paths.append(path)
    return paths


def _required_risk_evidence_ids(
    package: EvidencePackage,
    *,
    allowed_paths: set[str] | None = None,
) -> list[str]:
    ids: list[str] = []
    for signal in sorted(package.risk_signals, key=_risk_sort_key):
        primary_ids = _primary_evidence_ids_for_signal(
            package,
            signal,
            max_evidence_ids=1,
            expanded_only=True,
            allowed_paths=allowed_paths,
        )
        if primary_ids:
            ids.append(primary_ids[0])
            continue
        for evidence_id in signal.evidence_ids:
            evidence = package.evidence_index.get(evidence_id)
            if evidence is None:
                continue
            if (
                allowed_paths is not None
                and _path_for_evidence(evidence_id, evidence) not in allowed_paths
            ):
                continue
            ids.append(evidence_id)
            break
    return ids


def _required_evidence_satisfied(
    package: EvidencePackage,
    required_id: str,
    selected_ids: set[str],
) -> bool:
    if required_id in selected_ids:
        return True
    hunk_id = _hunk_evidence_id_for_line(package, required_id)
    return hunk_id is not None and hunk_id in selected_ids


def _first_diff_evidence_id(
    package: EvidencePackage,
    path: str | None,
) -> str | None:
    if path is None:
        return None
    for evidence_id, evidence in package.evidence_index.items():
        if evidence.kind == "diff_hunk" and _path_for_evidence(evidence_id, evidence) == path:
            return evidence_id
    for evidence_id, evidence in package.evidence_index.items():
        if evidence.kind == "diff" and _path_for_evidence(evidence_id, evidence) == path:
            return evidence_id
    return None


def _hunk_evidence_ids_for_change(
    package: EvidencePackage,
    change: DiffFileChange,
) -> list[str]:
    path = change.new_path or change.old_path
    if path is None:
        return []
    ids: list[str] = []
    for hunk in change.hunks:
        hunk_id = f"diff_hunk:{path}:{hunk.new_start or hunk.old_start or 1}"
        if hunk_id in package.evidence_index:
            ids.append(hunk_id)
    if ids:
        return ids
    first_diff = _first_diff_evidence_id(package, path)
    return [first_diff] if first_diff is not None else []


def _hunk_evidence_id_for_line(
    package: EvidencePackage,
    evidence_id: str,
) -> str | None:
    if evidence_id.startswith("diff_hunk:") and evidence_id in package.evidence_index:
        return evidence_id
    location = _diff_line_location(evidence_id)
    if location is None:
        return None
    path, line_number = location
    for change in package.changed_files:
        change_path = change.new_path or change.old_path
        if change_path != path:
            continue
        for hunk in change.hunks:
            if not (
                _line_in_range(line_number, hunk.new_start, hunk.new_count)
                or _line_in_range(line_number, hunk.old_start, hunk.old_count)
            ):
                continue
            hunk_id = f"diff_hunk:{path}:{hunk.new_start or hunk.old_start or 1}"
            if hunk_id in package.evidence_index:
                return hunk_id
    return None


def _diff_line_location(evidence_id: str) -> tuple[str, int] | None:
    parts = evidence_id.split(":")
    if len(parts) < 3 or parts[0] not in {"diff", "diff_hunk"} or not parts[-1].isdigit():
        return None
    return ":".join(parts[1:-1]), int(parts[-1])


def _line_in_range(line_number: int, start: int, count: int) -> bool:
    if count <= 0:
        return line_number == start
    return start <= line_number <= start + count - 1


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
    if evidence_id.startswith(("diff:", "diff_hunk:")):
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
        "context_profile": COMPACT_CONTEXT_PROFILE,
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


def _requested_evidence_ids_by_request(
    package: EvidencePackage,
    selected_ids: set[str],
    requests: list[ContextRequest],
    *,
    max_evidence_per_request: int,
) -> dict[int, list[str]]:
    requested_by_id: dict[int, list[str]] = {}
    for context_request in requests:
        requested_by_id[id(context_request)] = _requested_evidence_ids_for_request(
            package,
            selected_ids,
            context_request,
            max_evidence_per_request=max_evidence_per_request,
        )
    return requested_by_id


def _requested_evidence_ids_for_request(
    package: EvidencePackage,
    selected_ids: set[str],
    context_request: ContextRequest,
    *,
    max_evidence_per_request: int = DEFAULT_MAX_REFILL_EVIDENCE_PER_REQUEST,
) -> list[str]:
    explicit_ids = [
        evidence_id
        for evidence_id in context_request.evidence_ids
        if evidence_id in package.evidence_index and evidence_id not in selected_ids
    ]
    if explicit_ids:
        return _rank_refill_ids(
            package,
            _expand_explicit_refill_ids(package, explicit_ids),
            max_evidence_per_request,
        )

    requested: set[str] = set()
    if context_request.request_type == "same_file_more_evidence":
        if context_request.path is not None:
            requested.update(_evidence_ids_for_path(package, context_request.path))
    elif context_request.request_type == "related_tests":
        requested.update(_test_evidence_ids(package, context_request.path))
    elif context_request.request_type == "related_symbol":
        requested.update(_entity_evidence_ids(package, context_request.path))
    elif context_request.request_type == "risk_evidence":
        requested.update(_risk_related_evidence_ids(package, context_request))

    return _rank_refill_ids(
        package,
        [
            evidence_id
            for evidence_id in requested
            if evidence_id in package.evidence_index and evidence_id not in selected_ids
        ],
        max_evidence_per_request,
    )


def _rank_refill_ids(
    package: EvidencePackage,
    evidence_ids: list[str],
    limit: int,
) -> list[str]:
    candidates = [
        evidence_id
        for evidence_id in dict.fromkeys(evidence_ids)
        if evidence_id in package.evidence_index
    ]
    return sorted(
        candidates,
        key=lambda item: (-score_evidence(package, item), item),
    )[: max(0, limit)]


def _expand_explicit_refill_ids(
    package: EvidencePackage,
    evidence_ids: list[str],
) -> list[str]:
    expanded: list[str] = []
    for evidence_id in evidence_ids:
        expanded.append(evidence_id)
        evidence = package.evidence_index.get(evidence_id)
        if evidence is not None and evidence.kind == "diff":
            hunk_id = _hunk_evidence_id_for_line(package, evidence_id)
            if hunk_id is not None:
                expanded.append(hunk_id)
    return expanded


def _evidence_ids_for_path(package: EvidencePackage, path: str) -> set[str]:
    return set(EvidenceStore.from_legacy_package(package).ids_for_path(path))


def _store_item_path(store: EvidenceStore, evidence_id: str) -> str | None:
    item = store.get(evidence_id)
    return item.path if item is not None else None


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
    if len(parts) >= 3 and parts[0] == "diff_hunk":
        return ":".join(parts[1:-1])
    if len(parts) >= 3 and parts[0] == "entity":
        return parts[1]
    if len(parts) >= 3 and parts[0] == "risk":
        return ":".join(parts[2:])
    if len(parts) >= 2 and parts[0] in {"test_discovery", "hygiene"}:
        return parts[1]
    return None
