"""Deterministic grounding verifier for review-loop candidates."""

from __future__ import annotations

from dataclasses import dataclass, field

from code_review_agent.models import EvidencePackage, ReviewIssue


_STYLE_KEYWORDS: frozenset[str] = frozenset(
    {
        "blank line",
        "code style",
        "format",
        "import order",
        "indentation",
        "line length",
        "naming convention",
        "pep 8",
        "pep8",
        "style preference",
        "trailing space",
        "variable name",
        "whitespace",
    }
)


@dataclass(slots=True)
class GroundingDiscardedIssue:
    """A verifier-discarded issue plus the deterministic reason."""

    issue: ReviewIssue
    reason: str

    def to_dict(self) -> dict:
        data = self.issue.to_dict()
        data["filter_reason"] = self.reason
        return data


@dataclass(slots=True)
class VerifierResult:
    """Review issues partitioned before entering the critic."""

    verified: list[ReviewIssue] = field(default_factory=list)
    needs_human_review: list[ReviewIssue] = field(default_factory=list)
    discarded: list[GroundingDiscardedIssue] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "verified": [issue.to_dict() for issue in self.verified],
            "needs_human_review": [
                issue.to_dict() for issue in self.needs_human_review
            ],
            "discarded": [item.to_dict() for item in self.discarded],
        }


def ground_verify(
    issues: list[ReviewIssue],
    package: EvidencePackage,
    changed_paths: set[str],
) -> VerifierResult:
    """Partition candidate issues using deterministic evidence checks."""

    result = VerifierResult()

    def discard(issue: ReviewIssue, reason: str) -> None:
        result.discarded.append(GroundingDiscardedIssue(issue=issue, reason=reason))

    for issue in issues:
        if not issue.evidence_ids:
            discard(issue, "missing_evidence")
            continue

        if any(eid not in package.evidence_index for eid in issue.evidence_ids):
            discard(issue, "invalid_evidence_ids")
            continue

        if _is_style_preference(issue):
            discard(issue, "style_preference")
            continue

        if issue.file not in changed_paths:
            if not _has_related_changed_evidence(
                issue, package=package, changed_paths=changed_paths
            ):
                discard(issue, "file_not_changed")
                continue
            result.needs_human_review.append(issue)
            continue

        if not _line_is_related_to_change(issue, package):
            result.needs_human_review.append(issue)
            continue

        result.verified.append(issue)

    return result


def _is_style_preference(issue: ReviewIssue) -> bool:
    lower = issue.message.lower()
    return any(keyword in lower for keyword in _STYLE_KEYWORDS)


def _has_related_changed_evidence(
    issue: ReviewIssue, *, package: EvidencePackage, changed_paths: set[str]
) -> bool:
    for evidence_id in issue.evidence_ids:
        evidence = package.evidence_index.get(evidence_id)
        path = _path_from_evidence(evidence_id, evidence.source if evidence else None)
        if path in changed_paths:
            return True
    return False


def _line_is_related_to_change(issue: ReviewIssue, package: EvidencePackage) -> bool:
    if issue.line is None:
        return True
    if not _has_location_context_for_path(issue.file, package):
        return True
    if _line_in_changed_hunk(issue.file, issue.line, package):
        return True
    if _line_in_changed_entity(issue.file, issue.line, package):
        return True
    if _line_in_diff_evidence(issue, package):
        return True
    return False


def _has_location_context_for_path(path: str, package: EvidencePackage) -> bool:
    for change in package.changed_files:
        if path in {change.old_path, change.new_path}:
            return bool(change.hunks)
    return any(entity.path == path for entity in package.changed_entities)


def _line_in_changed_hunk(
    path: str, line_number: int, package: EvidencePackage
) -> bool:
    for change in package.changed_files:
        if path not in {change.old_path, change.new_path}:
            continue
        for hunk in change.hunks:
            if path == change.new_path and _line_in_range(
                line_number, hunk.new_start, hunk.new_count
            ):
                return True
            if path == change.old_path and _line_in_range(
                line_number, hunk.old_start, hunk.old_count
            ):
                return True
    return False


def _line_in_changed_entity(
    path: str, line_number: int, package: EvidencePackage
) -> bool:
    return any(
        entity.path == path and entity.line_start <= line_number <= entity.line_end
        for entity in package.changed_entities
    )


def _line_in_diff_evidence(issue: ReviewIssue, package: EvidencePackage) -> bool:
    for evidence_id in issue.evidence_ids:
        evidence = package.evidence_index.get(evidence_id)
        path, line_number = _diff_location_from_evidence(
            evidence_id, evidence.source if evidence else None
        )
        if path == issue.file and line_number == issue.line:
            return True
    return False


def _line_in_range(line_number: int, start: int, count: int) -> bool:
    if count <= 0:
        return line_number == start
    return start <= line_number <= start + count - 1


def _diff_location_from_evidence(
    evidence_id: str, source: str | None
) -> tuple[str | None, int | None]:
    parts = evidence_id.split(":")
    if len(parts) >= 3 and parts[0] == "diff":
        line = int(parts[-1]) if parts[-1].isdigit() else None
        return ":".join(parts[1:-1]), line

    if source and ":" in source:
        path, _, raw_line = source.rpartition(":")
        if raw_line.isdigit():
            return path, int(raw_line)
    return None, None


def _path_from_evidence(evidence_id: str, source: str | None) -> str | None:
    parts = evidence_id.split(":")
    if len(parts) >= 2 and parts[0] in {"entity", "hygiene", "test_discovery"}:
        return parts[1]
    if len(parts) >= 3 and parts[0] == "diff":
        return ":".join(parts[1:-1])
    if len(parts) >= 3 and parts[0] == "risk":
        return ":".join(parts[2:])
    if source is not None:
        return source.rsplit(":", 1)[0] if ":" in source else source
    return None
