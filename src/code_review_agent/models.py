"""Shared data models for the review pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Hygiene: evidence & semantic classification
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class HygieneEvidence:
    """All evidence gathered for a single file before LLM classification."""

    path: str
    content_sample: str
    imports: list[str] = field(default_factory=list)
    imported_by: list[str] = field(default_factory=list)
    referenced_by_tests: list[str] = field(default_factory=list)
    declared_in_config: list[str] = field(default_factory=list)
    folder_context: str | None = None
    previous_role: str | None = None
    signals: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SemanticClassification:
    """Result of LLM semantic classification for a single file."""

    path: str
    # One of the 7 taxonomy types defined in hygiene.taxonomy.
    artifact_type: str  # experiment_script | adhoc_script | process_doc | generated_artifact | demo_sample | obsolete_candidate | uncertain
    confidence: float
    suggested_action: str   # move | document | needs_human_review
    reason: str
    evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class FileClassification:
    path: str
    category: str
    mainline_relevance: str
    confidence: float
    reason: str
    signals: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class MoveSuggestion:
    source_path: str
    suggested_path: str
    category: str
    reason: str
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Context map and review pipeline models
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class SymbolSummary:
    """A Python class, function, or method with source line bounds."""

    path: str
    symbol_type: str
    name: str
    qualified_name: str
    line_start: int
    line_end: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PythonModuleSummary:
    """AST-derived summary for a Python module."""

    path: str
    module_docstring: str | None
    imports: list[str] = field(default_factory=list)
    classes: list[SymbolSummary] = field(default_factory=list)
    functions: list[SymbolSummary] = field(default_factory=list)
    methods: list[SymbolSummary] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class StyleBaseline:
    """Lightweight repository style baseline collected by RepoMapBuilder.

    Zero values are valid. Review risk rules can skip style checks when the
    sample is too small, such as total_public_functions < 5.
    """

    docstring_coverage_ratio: float = 0.0
    dominant_import_style: str = "mixed"
    test_naming_pattern: str | None = None
    dominant_exception_handling: str = "mixed"
    total_public_functions: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class RepoMap:
    """Machine-readable repository context used by review stages."""

    root: str
    files: list[str] = field(default_factory=list)
    python_modules: list[PythonModuleSummary] = field(default_factory=list)
    imports: dict[str, list[str]] = field(default_factory=dict)
    imported_by: dict[str, list[str]] = field(default_factory=dict)
    related_tests: dict[str, list[str]] = field(default_factory=dict)
    style_baseline: StyleBaseline | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DiffLine:
    """One line in a unified-diff hunk."""

    line_type: str
    old_lineno: int | None
    new_lineno: int | None
    content: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DiffHunk:
    """A parsed unified-diff hunk."""

    old_start: int
    old_count: int
    new_start: int
    new_count: int
    section_header: str
    lines: list[DiffLine] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DiffFileChange:
    """A file-level change from a unified diff."""

    old_path: str | None
    new_path: str | None
    change_type: str
    hunks: list[DiffHunk] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ChangedEntity:
    """A class/function/method/module affected by one or more hunks."""

    path: str
    entity_type: str
    name: str
    qualified_name: str
    line_start: int
    line_end: int
    hunk_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class RiskSignal:
    """A deterministic risk tag produced from diff and repo context."""

    tag: str
    confidence: float
    reason: str
    evidence_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ReviewEvidence:
    """A single traceable piece of evidence backing a ReviewIssue."""

    id: str                 # e.g. "diff:src/shop/service.py:35"
    kind: str               # "diff" | "entity" | "risk" | "test_discovery" | "hygiene"
    source: str             # file path or system check identifier
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ReviewIssue:
    file: str
    line: int | None
    severity: str
    category: str
    message: str
    suggestion: str
    confidence: float = 0.0
    evidence_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class EvidencePackage:
    """Structured context consumed by rules or constrained review agents."""

    repo_root: str
    changed_files: list[DiffFileChange] = field(default_factory=list)
    changed_entities: list[ChangedEntity] = field(default_factory=list)
    risk_signals: list[RiskSignal] = field(default_factory=list)
    evidence_index: dict[str, ReviewEvidence] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AgentRun:
    """Audit metadata for an optional review or critic agent invocation."""

    agent_name: str
    model: str | None
    prompt_hash: str | None
    input_evidence_ids: list[str] = field(default_factory=list)
    output_issue_ids: list[str] = field(default_factory=list)
    fallback_used: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ReviewReport:
    summary: dict[str, Any] = field(default_factory=dict)
    issues: list[ReviewIssue] = field(default_factory=list)
    file_classifications: list[FileClassification] = field(default_factory=list)
    move_suggestions: list[MoveSuggestion] = field(default_factory=list)
    semantic_classifications: list[SemanticClassification] = field(default_factory=list)
    uncertain_queue: list[SemanticClassification] = field(default_factory=list)
    project_artifacts_draft: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "issues": [issue.to_dict() for issue in self.issues],
            "file_classifications": [
                classification.to_dict()
                for classification in self.file_classifications
            ],
            "move_suggestions": [
                suggestion.to_dict()
                for suggestion in self.move_suggestions
            ],
            "semantic_classifications": [
                sc.to_dict() for sc in self.semantic_classifications
            ],
            "uncertain_queue": [
                sc.to_dict() for sc in self.uncertain_queue
            ],
            "project_artifacts_draft": self.project_artifacts_draft,
        }
