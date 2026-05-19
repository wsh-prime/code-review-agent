"""Review issue filter and misreport control layer."""

from __future__ import annotations

from dataclasses import dataclass, field

from code_review_agent.models import EvidencePackage, ReviewIssue
from code_review_agent.review.issue_quality import (
    is_low_signal_review_suggestion,
    is_style_preference,
)
from code_review_agent.review.schema import Finding, IssueLifecycleResult


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
    """Validate and partition legacy review issues.

    The implementation delegates to ``filter_findings`` so the main review path
    can use the compact lifecycle schema while older callers keep the same API.
    """

    candidates = [
        Finding.from_legacy_issue(issue, status="candidate")
        for issue in findings
    ]
    candidates.extend(
        Finding.from_legacy_issue(issue, status="needs_human_review")
        for issue in needs_human_review
    )
    lifecycle = filter_findings(
        candidates,
        package,
        changed_paths,
        confidence_threshold=confidence_threshold,
    )
    return FilterResult(
        findings=lifecycle.legacy_issues_by_status("finding"),
        needs_human_review=lifecycle.legacy_issues_by_status("needs_human_review"),
        discarded=[
            DiscardedIssue(
                issue=finding.to_legacy_issue(),
                reason=finding.reason or "discarded",
            )
            for finding in lifecycle.by_status("discarded")
        ],
    )


def filter_findings(
    candidates: list[Finding],
    package: EvidencePackage,
    changed_paths: set[str],
    *,
    confidence_threshold: float = 0.6,
) -> IssueLifecycleResult:
    """Validate and partition review findings.

    The filter is deliberately conservative: an issue with no valid evidence is
    discarded, while location uncertainty and low confidence are downgraded to
    ``needs_human_review``.
    """

    result = IssueLifecycleResult()

    def emit(finding: Finding, status: str, reason: str = "") -> None:
        result.items.append(_finding_with(finding, status=status, reason=reason))

    def route_finding(finding: Finding) -> None:
        issue = finding.to_legacy_issue()
        if not finding.evidence_ids:
            emit(finding, "discarded", "missing_evidence")
            return

        valid_ids = [
            eid for eid in finding.evidence_ids if eid in package.evidence_index
        ]
        if not valid_ids:
            emit(finding, "discarded", "invalid_evidence_ids")
            return

        clean_finding = _finding_with(finding, evidence_ids=valid_ids)
        clean_issue = clean_finding.to_legacy_issue()

        if is_style_preference(clean_issue):
            emit(clean_finding, "discarded", "style_preference")
            return
        if is_low_signal_review_suggestion(clean_issue):
            emit(clean_finding, "discarded", "low_signal_suggestion")
            return

        if clean_issue.file not in changed_paths:
            if not _has_related_changed_evidence(
                clean_issue, package=package, changed_paths=changed_paths
            ):
                emit(clean_finding, "discarded", "file_not_changed")
                return
            emit(clean_finding, "needs_human_review", "related_file")
            return

        if not _line_is_related_to_change(clean_issue, package):
            emit(clean_finding, "needs_human_review", "line_uncertain")
            return

        if clean_finding.status == "needs_human_review":
            emit(clean_finding, "needs_human_review", clean_finding.reason)
            return
        if clean_issue.confidence < confidence_threshold:
            emit(clean_finding, "needs_human_review", "low_confidence")
            return

        emit(clean_finding, "finding")

    for finding in candidates:
        route_finding(finding)

    result.items = [
        *_merge_duplicate_findings(result.by_status("finding")),
        *_merge_duplicate_findings(result.by_status("needs_human_review")),
        *result.by_status("discarded"),
    ]
    return result


def _finding_with(
    finding: Finding,
    *,
    status: str | None = None,
    reason: str | None = None,
    evidence_ids: list[str] | None = None,
) -> Finding:
    return Finding(
        file=finding.file,
        line=finding.line,
        severity=finding.severity,
        category=finding.category,
        message=finding.message,
        suggestion=finding.suggestion,
        confidence=finding.confidence,
        evidence_ids=(
            list(finding.evidence_ids) if evidence_ids is None else list(evidence_ids)
        ),
        status=finding.status if status is None else status,
        reason=finding.reason if reason is None else reason,
    )


def _merge_duplicate_findings(findings: list[Finding]) -> list[Finding]:
    merged_issues = _merge_duplicates(
        [finding.to_legacy_issue() for finding in findings]
    )
    reason_by_key = {
        (finding.file, finding.category): finding.reason
        for finding in findings
        if finding.reason
    }
    status_by_key = {
        (finding.file, finding.category): finding.status
        for finding in findings
    }
    return [
        Finding.from_legacy_issue(
            issue,
            status=status_by_key.get((issue.file, issue.category), "candidate"),
            reason=reason_by_key.get((issue.file, issue.category), ""),
        )
        for issue in merged_issues
    ]


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
    if len(parts) >= 3 and parts[0] in {"diff", "diff_hunk"}:
        return ":".join(parts[1:-1])
    if len(parts) >= 3 and parts[0] == "risk":
        return ":".join(parts[2:])
    if source is not None:
        return source.rsplit(":", 1)[0] if ":" in source else source
    return None
