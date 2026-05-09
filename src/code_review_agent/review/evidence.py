"""Build EvidencePackage objects for review rules and constrained agents."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from code_review_agent.models import (
    ChangedEntity,
    DiffFileChange,
    DiffHunk,
    DiffLine,
    EvidencePackage,
    FileClassification,
    RepoMap,
    ReviewEvidence,
    RiskSignal,
)
from code_review_agent.review.risk import (
    diff_evidence_id,
    diff_hunk_evidence_id,
    entity_evidence_id,
    hygiene_evidence_id,
    risk_evidence_id,
    test_discovery_evidence_id,
)


REDACTED_METADATA_FIELDS = [
    "pr_title",
    "pr_description",
    "commit_message",
    "author",
    "reviewer",
]
MAX_HUNK_EVIDENCE_LINES = 80
MAX_HUNK_LINE_CHARS = 200


def build_evidence_package(
    repo_path: Path | str,
    changes: list[DiffFileChange],
    changed_entities: list[ChangedEntity],
    risk_signals: list[RiskSignal],
    repo_map: RepoMap,
    *,
    hygiene_classifications: list[FileClassification] | None = None,
) -> EvidencePackage:
    """Collect traceable evidence for a review run."""

    evidence_index: dict[str, ReviewEvidence] = {}
    _add_many(evidence_index, _diff_evidence(changes))
    _add_many(evidence_index, _entity_evidence(changed_entities))
    _add_many(evidence_index, _test_discovery_evidence(repo_map))
    _add_many(evidence_index, _hygiene_evidence(hygiene_classifications or []))
    _add_many(evidence_index, _risk_evidence(risk_signals))

    return EvidencePackage(
        repo_root=str(Path(repo_path).resolve()),
        changed_files=changes,
        changed_entities=changed_entities,
        risk_signals=risk_signals,
        evidence_index=evidence_index,
        metadata={
            "redacted": REDACTED_METADATA_FIELDS,
            "target_repo_modified": False,
        },
    )


def find_missing_evidence_ids(
    package: EvidencePackage,
    *,
    issues: list | None = None,
) -> list[str]:
    """Return evidence ID references that do not exist in the evidence index.

    Checks both ``RiskSignal.evidence_ids`` and, when *issues* is supplied,
    each ``ReviewIssue.evidence_ids`` list.  The review pipeline passes
    pre-filter candidate issues so JSON reports can audit ghost IDs even when
    the formal filter discards the candidate later.
    """

    missing: set[str] = set()
    for risk in package.risk_signals:
        for evidence_id in risk.evidence_ids:
            if evidence_id not in package.evidence_index:
                missing.add(evidence_id)
    for issue in issues or []:
        for evidence_id in issue.evidence_ids:
            if evidence_id not in package.evidence_index:
                missing.add(evidence_id)
    return sorted(missing)


def _diff_evidence(changes: list[DiffFileChange]) -> list[ReviewEvidence]:
    evidence: list[ReviewEvidence] = []
    for change in changes:
        path = _change_path(change)
        if path is None:
            continue
        if not change.hunks:
            evidence.append(
                ReviewEvidence(
                    id=diff_evidence_id(path, 1),
                    kind="diff",
                    source=f"{path}:1",
                    message=f"{change.change_type} file change without text hunks.",
                )
            )
            continue

        for hunk in change.hunks:
            evidence.append(_hunk_evidence(path, hunk))
            for line in hunk.lines:
                if line.line_type not in {"added", "removed"}:
                    continue
                line_number = _line_number(line)
                evidence.append(
                    ReviewEvidence(
                        id=diff_evidence_id(path, line_number),
                        kind="diff",
                        source=f"{path}:{line_number}",
                        message=_diff_line_message(line),
                    )
                )
    return evidence


def _hunk_evidence(path: str, hunk: DiffHunk) -> ReviewEvidence:
    start_line = _hunk_start_line(hunk)
    return ReviewEvidence(
        id=diff_hunk_evidence_id(path, start_line),
        kind="diff_hunk",
        source=f"{path}:{start_line}",
        message=_diff_hunk_message(hunk),
    )


def _entity_evidence(entities: list[ChangedEntity]) -> list[ReviewEvidence]:
    evidence: list[ReviewEvidence] = []
    for entity in entities:
        evidence.append(
            ReviewEvidence(
                id=entity_evidence_id(entity),
                kind="entity",
                source=f"{entity.path}:{entity.line_start}-{entity.line_end}",
                message=(
                    f"Changed {entity.entity_type} "
                    f"{entity.qualified_name} touched by {len(entity.hunk_ids)} hunk(s)."
                ),
            )
        )
    return evidence


def _risk_evidence(signals: list[RiskSignal]) -> list[ReviewEvidence]:
    evidence: list[ReviewEvidence] = []
    for signal in signals:
        evidence.append(
            ReviewEvidence(
                id=risk_evidence_id(signal),
                kind="risk",
                source=signal.tag,
                message=signal.reason,
            )
        )
    return evidence


def _test_discovery_evidence(repo_map: RepoMap) -> list[ReviewEvidence]:
    evidence: list[ReviewEvidence] = []
    seen: set[str] = set()
    for source_path, related_tests in repo_map.related_tests.items():
        for test_path in related_tests:
            if test_path in seen:
                continue
            seen.add(test_path)
            evidence.append(
                ReviewEvidence(
                    id=test_discovery_evidence_id(test_path),
                    kind="test_discovery",
                    source=test_path,
                    message=f"Related test discovered for {source_path}.",
                )
            )
    return evidence


def _hygiene_evidence(
    classifications: list[FileClassification],
) -> list[ReviewEvidence]:
    evidence: list[ReviewEvidence] = []
    for classification in classifications:
        evidence.append(
            ReviewEvidence(
                id=hygiene_evidence_id(classification.path),
                kind="hygiene",
                source=classification.path,
                message=(
                    f"Hygiene category {classification.category} "
                    f"({classification.confidence:.2f}): {classification.reason}"
                ),
            )
        )
    return evidence


def _add_many(
    evidence_index: dict[str, ReviewEvidence],
    evidence_items: Iterable[ReviewEvidence],
) -> None:
    for evidence in evidence_items:
        evidence_index[evidence.id] = evidence


def _diff_line_message(line: DiffLine) -> str:
    action = "Added" if line.line_type == "added" else "Removed"
    content = line.content.strip()
    if len(content) > 120:
        content = f"{content[:117]}..."
    return f"{action} line: {content}"


def _diff_hunk_message(hunk: DiffHunk) -> str:
    header = (
        f"@@ -{hunk.old_start},{hunk.old_count} "
        f"+{hunk.new_start},{hunk.new_count} @@ {hunk.section_header}".rstrip()
    )
    lines = [header]
    omitted_count = max(0, len(hunk.lines) - MAX_HUNK_EVIDENCE_LINES)
    for line in hunk.lines[:MAX_HUNK_EVIDENCE_LINES]:
        prefix = _diff_prefix(line)
        content = line.content
        if len(content) > MAX_HUNK_LINE_CHARS:
            content = f"{content[:MAX_HUNK_LINE_CHARS - 3]}..."
        lines.append(f"{prefix}{content}")
    if omitted_count:
        lines.append(f"... omitted {omitted_count} hunk line(s)")
    return "\n".join(lines)


def _diff_prefix(line: DiffLine) -> str:
    if line.line_type == "added":
        return "+"
    if line.line_type == "removed":
        return "-"
    return " "


def _line_number(line: DiffLine) -> int:
    return line.new_lineno or line.old_lineno or 1


def _hunk_start_line(hunk: DiffHunk) -> int:
    return hunk.new_start or hunk.old_start or 1


def _change_path(change: DiffFileChange) -> str | None:
    return change.new_path or change.old_path
