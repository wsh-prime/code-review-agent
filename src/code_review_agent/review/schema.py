"""Compact review-domain schema and legacy adapters.

The legacy pipeline still uses the shared dataclasses in ``models.py``.  This
module defines the smaller conceptual model we are migrating toward and provides
lossless-enough adapters so individual stages can move without a big rewrite.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from code_review_agent.models import DiffFileChange, EvidencePackage, ReviewIssue


@dataclass(slots=True)
class TextRange:
    """A file span on either the old or new side of a change."""

    path: str
    start_line: int | None = None
    end_line: int | None = None
    side: str = "new"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ChangeHunk:
    """One unified-diff hunk in a changed file."""

    id: str
    path: str
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    section_header: str = ""
    changed_line_count: int = 0
    evidence_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ChangedFile:
    """A file-level change plus hunk IDs and lightweight metadata."""

    path: str
    change_type: str
    old_path: str | None = None
    new_path: str | None = None
    language: str = "unknown"
    file_role: str = "unknown"
    hunks: list[ChangeHunk] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ChangeSet:
    """The review input: repository root, changed files, and run metadata."""

    repo_root: str
    files: list[ChangedFile] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_legacy_package(cls, package: EvidencePackage) -> "ChangeSet":
        return cls(
            repo_root=package.repo_root,
            files=[_changed_file_from_legacy(change) for change in package.changed_files],
            metadata=dict(package.metadata),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class EvidenceItem:
    """One citable or refillable unit of review context."""

    id: str
    type: str
    path: str | None
    text: str
    source: str = ""
    range: TextRange | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    links: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class EvidenceStore:
    """Queryable evidence pool keyed by evidence ID."""

    items: dict[str, EvidenceItem] = field(default_factory=dict)

    @classmethod
    def from_legacy_package(cls, package: EvidencePackage) -> "EvidenceStore":
        items: dict[str, EvidenceItem] = {}
        for evidence_id, evidence in package.evidence_index.items():
            path = _path_from_evidence_id(evidence_id, evidence.source)
            items[evidence_id] = EvidenceItem(
                id=evidence_id,
                type=evidence.kind,
                path=path,
                text=evidence.message,
                source=evidence.source,
                range=_range_from_evidence(evidence_id, evidence.source, path),
            )
        return cls(items=items)

    def get(self, evidence_id: str) -> EvidenceItem | None:
        return self.items.get(evidence_id)

    def ids(self) -> list[str]:
        return sorted(self.items)

    def ids_for_path(self, path: str) -> list[str]:
        return sorted(
            evidence_id
            for evidence_id, item in self.items.items()
            if item.path == path
        )

    def ids_for_type(self, evidence_type: str) -> list[str]:
        return sorted(
            evidence_id
            for evidence_id, item in self.items.items()
            if item.type == evidence_type
        )

    def ids_for_path_and_type(self, path: str, evidence_type: str) -> list[str]:
        return sorted(
            evidence_id
            for evidence_id, item in self.items.items()
            if item.path == path and item.type == evidence_type
        )

    def to_dict(self) -> dict[str, Any]:
        return {key: item.to_dict() for key, item in self.items.items()}


@dataclass(slots=True)
class ReviewContext:
    """A budgeted evidence slice to send to a reviewer."""

    id: str
    evidence_ids: list[str] = field(default_factory=list)
    rules: list[dict[str, Any]] = field(default_factory=list)
    available_evidence: dict[str, Any] = field(default_factory=dict)
    budget: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Finding:
    """A review issue with explicit lifecycle status."""

    file: str
    line: int | None
    message: str
    suggestion: str
    severity: str = "medium"
    category: str = "correctness"
    confidence: float = 0.0
    evidence_ids: list[str] = field(default_factory=list)
    status: str = "candidate"
    reason: str = ""

    @classmethod
    def from_legacy_issue(
        cls,
        issue: ReviewIssue,
        *,
        status: str = "candidate",
        reason: str = "",
    ) -> "Finding":
        return cls(
            file=issue.file,
            line=issue.line,
            message=issue.message,
            suggestion=issue.suggestion,
            severity=issue.severity,
            category=issue.category,
            confidence=issue.confidence,
            evidence_ids=list(issue.evidence_ids),
            status=status,
            reason=reason,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_legacy_issue(self) -> ReviewIssue:
        """Convert this finding back to the legacy issue contract."""

        return ReviewIssue(
            file=self.file,
            line=self.line,
            severity=self.severity,
            category=self.category,
            message=self.message,
            suggestion=self.suggestion,
            confidence=self.confidence,
            evidence_ids=list(self.evidence_ids),
        )


@dataclass(slots=True)
class IssueLifecycleResult:
    """Unified finding lifecycle ledger with legacy bucket adapters."""

    items: list[Finding] = field(default_factory=list)

    @classmethod
    def from_legacy_buckets(
        cls,
        *,
        findings: list[ReviewIssue],
        needs_human_review: list[ReviewIssue],
        discarded: list[dict[str, Any]],
    ) -> "IssueLifecycleResult":
        items = [
            Finding.from_legacy_issue(issue, status="finding")
            for issue in findings
        ]
        items.extend(
            Finding.from_legacy_issue(issue, status="needs_human_review")
            for issue in needs_human_review
        )
        for item in discarded:
            reason = str(item.get("filter_reason") or item.get("reason") or "")
            issue = ReviewIssue(
                file=str(item.get("file", "patch")),
                line=_optional_int(item.get("line")),
                severity=str(item.get("severity", "medium")),
                category=str(item.get("category", "discarded")),
                message=str(item.get("message", "")),
                suggestion=str(item.get("suggestion", "")),
                confidence=_optional_float(item.get("confidence"), default=0.0),
                evidence_ids=[str(eid) for eid in item.get("evidence_ids", [])],
            )
            items.append(
                Finding.from_legacy_issue(
                    issue,
                    status="discarded",
                    reason=reason,
                )
            )
        return cls(items=items)

    def by_status(self, status: str) -> list[Finding]:
        return [item for item in self.items if item.status == status]

    def legacy_issues_by_status(self, status: str) -> list[ReviewIssue]:
        return [item.to_legacy_issue() for item in self.by_status(status)]

    def counts_by_status(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.items:
            counts[item.status] = counts.get(item.status, 0) + 1
        return counts

    def to_dict(self) -> dict[str, Any]:
        return {
            "items": [item.to_dict() for item in self.items],
            "counts_by_status": self.counts_by_status(),
        }


@dataclass(slots=True)
class RunTrace:
    """Operational audit for a review run."""

    run_id: str = ""
    shards: list[dict[str, Any]] = field(default_factory=list)
    agent_runs: list[dict[str, Any]] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _changed_file_from_legacy(change: DiffFileChange) -> ChangedFile:
    path = change.new_path or change.old_path or "<unknown>"
    return ChangedFile(
        path=path,
        old_path=change.old_path,
        new_path=change.new_path,
        change_type=change.change_type,
        language=_language_for_path(path),
        file_role=_file_role(path),
        hunks=[
            ChangeHunk(
                id=_hunk_id(path, hunk.new_start or hunk.old_start or 1),
                path=path,
                old_start=hunk.old_start,
                old_count=hunk.old_count,
                new_start=hunk.new_start,
                new_count=hunk.new_count,
                section_header=hunk.section_header,
                changed_line_count=sum(
                    1
                    for line in hunk.lines
                    if line.line_type in {"added", "removed"}
                ),
                evidence_id=_hunk_id(path, hunk.new_start or hunk.old_start or 1),
            )
            for hunk in change.hunks
        ],
    )


def _hunk_id(path: str, start_line: int) -> str:
    return f"diff_hunk:{path}:{start_line}"


def _path_from_evidence_id(evidence_id: str, source: str) -> str | None:
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
    if source and ":" in source:
        return source.rsplit(":", 1)[0]
    return source or None


def _range_from_evidence(
    evidence_id: str,
    source: str,
    path: str | None,
) -> TextRange | None:
    if path is None:
        return None
    line = _line_from_evidence_id(evidence_id)
    if line is None and source and ":" in source:
        _, _, raw_line = source.rpartition(":")
        line = int(raw_line) if raw_line.isdigit() else None
    if line is None:
        return TextRange(path=path)
    return TextRange(path=path, start_line=line, end_line=line)


def _line_from_evidence_id(evidence_id: str) -> int | None:
    parts = evidence_id.split(":")
    if len(parts) >= 3 and parts[0] in {"diff", "diff_hunk"} and parts[-1].isdigit():
        return int(parts[-1])
    return None


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _optional_float(value: object, *, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _language_for_path(path: str) -> str:
    suffix = path.rsplit(".", 1)[-1].lower() if "." in path else ""
    return {
        "py": "python",
        "js": "javascript",
        "jsx": "javascript",
        "ts": "typescript",
        "tsx": "typescript",
        "cs": "csharp",
        "java": "java",
        "go": "go",
        "rs": "rust",
        "md": "markdown",
        "json": "json",
        "yml": "yaml",
        "yaml": "yaml",
        "toml": "toml",
    }.get(suffix, "unknown")


def _file_role(path: str) -> str:
    normalized = path.replace("\\", "/")
    name = normalized.rsplit("/", 1)[-1].lower()
    if normalized.startswith("docs/") or name.endswith((".md", ".rst", ".txt")):
        return "docs"
    if "/test/" in f"/{normalized}/" or name.startswith("test_") or name.endswith(
        (".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx")
    ):
        return "test"
    if name in {"pyproject.toml", "package.json", "tsconfig.json"} or normalized.startswith(
        ".github/workflows/"
    ):
        return "config"
    if normalized.startswith(("src/", "lib/", "app/", "apps/", "packages/")):
        return "source"
    return "other"
