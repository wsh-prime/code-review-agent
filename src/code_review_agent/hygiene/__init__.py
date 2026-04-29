"""Project Hygiene Review modules."""

from code_review_agent.hygiene.classifier import (
    classify_file,
    classify_files,
    classify_files_semantic,
    index_classifications_by_path,
)
from code_review_agent.hygiene.evidence import (
    collect_evidence,
    is_safety_guard_triggered,
)
from code_review_agent.hygiene.llm_classifier import (
    FakeLLMClassifier,
    LLMClassifier,
    classify_with_llm,
    validate_semantic_classification,
)
from code_review_agent.hygiene.planner import (
    build_move_suggestions,
    build_move_suggestions_from_semantic,
    build_project_artifacts_draft,
    build_uncertain_queue,
)
from code_review_agent.hygiene.scanner import ScannedFile, scan_repository
from code_review_agent.hygiene.taxonomy import (
    ALL_TYPES,
    DESCRIPTIONS,
    SUGGESTED_ACTIONS,
    TARGET_DIRS,
)

__all__ = [
    # scanner
    "ScannedFile",
    "scan_repository",
    # classifier (rules)
    "classify_file",
    "classify_files",
    "classify_files_semantic",
    "index_classifications_by_path",
    # evidence
    "collect_evidence",
    "is_safety_guard_triggered",
    # llm_classifier
    "FakeLLMClassifier",
    "LLMClassifier",
    "classify_with_llm",
    "validate_semantic_classification",
    # planner
    "build_move_suggestions",
    "build_move_suggestions_from_semantic",
    "build_project_artifacts_draft",
    "build_uncertain_queue",
    # taxonomy
    "ALL_TYPES",
    "DESCRIPTIONS",
    "SUGGESTED_ACTIONS",
    "TARGET_DIRS",
]
