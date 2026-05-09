"""Review issue filter and misreport control layer."""

from __future__ import annotations

from dataclasses import dataclass, field

from code_review_agent.models import EvidencePackage, ReviewIssue
from code_review_agent.review.issue_quality import (
    is_low_signal_review_suggestion,
    is_style_preference,
)


@dataclass(slots=True)
class DiscardedIssue:
    """A discarded issue plus the filter reason for JSON audit trails."""

    issue: ReviewIssue
    reason: str

    def to_dict(self) -> dict:
        data = self.issue.to_dict()
        data["filter_reason"] = self.reason
        return data


@dataclass(slots=True)
class FilterResult:
    """Issues partitioned by actionability after filtering."""

    findings: list[ReviewIssue] = field(default_factory=list)
    needs_human_review: list[ReviewIssue] = field(default_factory=list)
    discarded: list[DiscardedIssue] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "findings": [issue.to_dict() for issue in self.findings],
            "needs_human_review": [
                issue.to_dict() for issue in self.needs_human_review
            ],
            "discarded": [issue.to_dict() for issue in self.discarded],
        }


def filter_issues(
    findings: list[ReviewIssue],
    needs_human_review: list[ReviewIssue],
    package: EvidencePackage,
    changed_paths: set[str],
    *,
    confidence_threshold: float = 0.6,
) -> FilterResult:
    """Validate and partition review issues.

    The filter is deliberately conservative: an issue with no valid evidence is
    discarded, while location uncertainty and low confidence are downgraded to
    ``needs_human_review``.
    """

    result = FilterResult()

    def discard(issue: ReviewIssue, reason: str) -> None:
        result.discarded.append(DiscardedIssue(issue=issue, reason=reason))

    def route_issue(issue: ReviewIssue, *, already_uncertain: bool) -> None:
        if not issue.evidence_ids:
            discard(issue, "missing_evidence")
            return

        valid_ids = [eid for eid in issue.evidence_ids if eid in package.evidence_index]
        if not valid_ids:
            discard(issue, "invalid_evidence_ids")
            return

        clean_issue = ReviewIssue(
            file=issue.file,
            line=issue.line,
            severity=issue.severity,
            category=issue.category,
            message=issue.message,
            suggestion=issue.suggestion,
            confidence=issue.confidence,
            evidence_ids=valid_ids,
        )

        if is_style_preference(clean_issue):
            discard(clean_issue, "style_preference")
            return
        if is_low_signal_review_suggestion(clean_issue):
            discard(clean_issue, "low_signal_suggestion")
            return

        if clean_issue.file not in changed_paths:
            if not _has_related_changed_evidence(
                clean_issue, package=package, changed_paths=changed_paths
            ):
                discard(clean_issue, "file_not_changed")
                return
            result.needs_human_review.append(clean_issue)
            return

        if not _line_is_related_to_change(clean_issue, package):
            result.needs_human_review.append(clean_issue)
            return

        if already_uncertain or clean_issue.confidence < confidence_threshold:
            result.needs_human_review.append(clean_issue)
            return

        result.findings.append(clean_issue)

    for issue in findings:
        route_issue(issue, already_uncertain=False)
    for issue in needs_human_review:
        route_issue(issue, already_uncertain=True)

    result.findings = _merge_duplicates(result.findings)
    result.needs_human_review = _merge_duplicates(result.needs_human_review)
    return result


def _merge_duplicates(issues: list[ReviewIssue]) -> list[ReviewIssue]:
    """Merge duplicate issues, keeping the highest-confidence wording."""

    seen: dict[tuple[str, str], ReviewIssue] = {}
    for issue in issues:
        key = (issue.file, issue.category)
        existing = seen.get(key)
        if existing is None:
            seen[key] = issue
            continue

        winner = existing if existing.confidence >= issue.confidence else issue
        evidence_ids = sorted(dict.fromkeys(existing.evidence_ids + issue.evidence_ids))
        seen[key] = ReviewIssue(
            file=winner.file,
            line=winner.line,
            severity=winner.severity,
            category=winner.category,
            message=winner.message,
            suggestion=winner.suggestion,
            confidence=max(existing.confidence, issue.confidence),
            evidence_ids=evidence_ids,
        )

    return list(seen.values())


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
