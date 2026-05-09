"""Rules-only review findings built from deterministic risk signals."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from code_review_agent.models import EvidencePackage, ReviewIssue, RiskSignal
from code_review_agent.review.risk import (
    DEPENDENCY_CHANGE,
    ERROR_HANDLING_CHANGE,
    EXPERIMENT_ARTIFACT,
    TEST_GAP,
    risk_evidence_id,
)

MAX_RULE_ISSUE_EVIDENCE_IDS = 12


@dataclass(slots=True)
class RulesReviewResult:
    """Findings split by whether they should be surfaced immediately."""

    findings: list[ReviewIssue] = field(default_factory=list)
    needs_human_review: list[ReviewIssue] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "findings": [issue.to_dict() for issue in self.findings],
            "needs_human_review": [
                issue.to_dict() for issue in self.needs_human_review
            ],
        }


def run_rules(package: EvidencePackage) -> RulesReviewResult:
    """Convert high-signal risks into evidence-backed review issues."""

    result = RulesReviewResult()
    for signal in package.risk_signals:
        if signal.tag == TEST_GAP:
            result.findings.append(_test_gap_issue(signal, package))
        elif signal.tag == EXPERIMENT_ARTIFACT and _is_mainline_or_root_signal(signal):
            result.findings.append(_experiment_artifact_issue(signal, package))
        elif signal.tag == ERROR_HANDLING_CHANGE and _has_added_broad_exception(signal, package):
            result.findings.append(_broad_exception_issue(signal, package))
        elif signal.tag == DEPENDENCY_CHANGE:
            result.needs_human_review.append(_dependency_issue(signal, package))

    return result


def _test_gap_issue(signal: RiskSignal, package: EvidencePackage) -> ReviewIssue:
    path, line = _first_changed_location(signal, package)
    return ReviewIssue(
        file=path,
        line=line,
        severity="medium",
        category=TEST_GAP,
        message="Business logic changed while related tests exist but were not updated.",
        suggestion="Update the related test coverage or explain why the existing tests still cover this change.",
        confidence=max(signal.confidence, 0.75),
        evidence_ids=_issue_evidence_ids(signal, package),
    )


def _experiment_artifact_issue(
    signal: RiskSignal, package: EvidencePackage
) -> ReviewIssue:
    path, line = _first_changed_location(signal, package)
    return ReviewIssue(
        file=path,
        line=line,
        severity="medium",
        category=EXPERIMENT_ARTIFACT,
        message="A process or experiment artifact appears to have been added to mainline code.",
        suggestion="Move the artifact under a dedicated experiments, scripts, or docs area before merging.",
        confidence=max(signal.confidence, 0.7),
        evidence_ids=_issue_evidence_ids(signal, package),
    )


def _broad_exception_issue(signal: RiskSignal, package: EvidencePackage) -> ReviewIssue:
    path, line = _first_changed_location(signal, package)
    return ReviewIssue(
        file=path,
        line=line,
        severity="medium",
        category=ERROR_HANDLING_CHANGE,
        message="Broad exception handling was added in non-test code.",
        suggestion="Catch a narrower exception or preserve failure context so unexpected errors are not hidden.",
        confidence=max(signal.confidence, 0.7),
        evidence_ids=_issue_evidence_ids(signal, package),
    )


def _dependency_issue(signal: RiskSignal, package: EvidencePackage) -> ReviewIssue:
    path, line = _first_changed_location(signal, package)
    return ReviewIssue(
        file=path,
        line=line,
        severity="low",
        category=DEPENDENCY_CHANGE,
        message="Dependency declarations changed and should be reviewed with install/test impact in mind.",
        suggestion="Confirm lock files, compatibility, and test coverage for the dependency change.",
        confidence=min(max(signal.confidence, 0.6), 0.75),
        evidence_ids=_issue_evidence_ids(signal, package),
    )


def _issue_evidence_ids(
    signal: RiskSignal, package: EvidencePackage
) -> list[str]:
    evidence_ids = list(signal.evidence_ids[:MAX_RULE_ISSUE_EVIDENCE_IDS])
    signal_evidence_id = risk_evidence_id(signal)
    if signal_evidence_id in package.evidence_index:
        evidence_ids.insert(0, signal_evidence_id)
    return sorted(dict.fromkeys(evidence_ids))


def _first_changed_location(
    signal: RiskSignal, package: EvidencePackage
) -> tuple[str, int | None]:
    for evidence_id in signal.evidence_ids:
        if not evidence_id.startswith("diff:"):
            continue
        parts = evidence_id.split(":")
        if len(parts) >= 3:
            line = int(parts[2]) if parts[2].isdigit() else None
            return parts[1], line

    path = _first_path_from_signal(signal)
    if path:
        return path, None

    for change in package.changed_files:
        path = change.new_path or change.old_path
        if path is not None:
            return path, None
    return "patch", None


def _first_path_from_signal(signal: RiskSignal) -> str | None:
    for evidence_id in signal.evidence_ids:
        parts = evidence_id.split(":")
        if len(parts) >= 2 and parts[0] in {"entity", "hygiene", "diff", "diff_hunk"}:
            return parts[1]
    return None


def _is_mainline_or_root_signal(signal: RiskSignal) -> bool:
    path = _first_path_from_signal(signal)
    if path is None:
        return False
    parts = Path(path).parts
    return len(parts) == 1 or (bool(parts) and parts[0] == "src")


def _has_added_broad_exception(
    signal: RiskSignal, package: EvidencePackage
) -> bool:
    path, _ = _first_changed_location(signal, package)
    if _is_test_path(path) or not path.endswith(".py"):
        return False

    for change in package.changed_files:
        change_path = change.new_path or change.old_path
        if change_path != path:
            continue
        for hunk in change.hunks:
            for line in hunk.lines:
                if line.line_type != "added":
                    continue
                stripped = line.content.strip()
                if stripped.startswith("except Exception") or stripped == "except:":
                    return True
    return False


def _is_test_path(path: str) -> bool:
    parts = Path(path).parts
    name = Path(path).name
    return "tests" in parts or name.startswith("test_") or name.endswith("_test.py")
