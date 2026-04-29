"""Rule-based file classification for Project Hygiene Review."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from code_review_agent.hygiene.evidence import (
    build_module_path_index,
    collect_evidence,
    is_safety_guard_triggered,
    resolve_import,
    extract_import_names,
)
from code_review_agent.hygiene.llm_classifier import LLMClassifier, classify_with_llm
from code_review_agent.hygiene.scanner import ScannedFile
from code_review_agent.models import FileClassification, SemanticClassification


MAIN_CODE = "main_code"
TEST_CODE = "test_code"
DATA_SCRIPT = "data_script"
DEV_SCRIPT = "dev_script"
EXPERIMENT = "experiment"
DESIGN_DOC = "design_doc"
RESEARCH_DOC = "research_doc"
PLANNING_DOC = "planning_doc"
TODO = "todo"
ARTIFACT = "artifact"
UNKNOWN = "unknown"

PROCESS_CATEGORIES = {
    DATA_SCRIPT,
    DEV_SCRIPT,
    EXPERIMENT,
    RESEARCH_DOC,
    PLANNING_DOC,
    TODO,
    ARTIFACT,
}


def classify_files(
    repo_path: Path | str,
    scanned_files: list[ScannedFile],
) -> list[FileClassification]:
    """Classify scanned files using deterministic path/content signals."""

    root = Path(repo_path)
    imported_paths = _find_imported_local_python_paths(root, scanned_files)
    classifications = [
        classify_file(file, imported_paths=imported_paths)
        for file in scanned_files
    ]
    return sorted(classifications, key=lambda item: item.path)


def index_classifications_by_path(
    classifications: list[FileClassification],
) -> dict[str, FileClassification]:
    """Index classifications for later diff/context pipeline consumption."""

    return {classification.path: classification for classification in classifications}


def classify_file(
    file: ScannedFile,
    *,
    imported_paths: set[str] | None = None,
) -> FileClassification:
    imported_paths = imported_paths or set()
    path = file.path
    parts = path.split("/")
    name = parts[-1]
    lower_path = path.lower()
    lower_name = name.lower()
    sample = file.content_sample.lower()
    signals: list[str] = []

    if path in imported_paths and file.extension == ".py":
        signals.append("python file is imported by another local module")
        return _classification(
            path,
            MAIN_CODE,
            "high",
            0.94,
            "Python file is referenced by local package imports, so it should stay in the mainline.",
            signals,
        )

    if _is_readme(name):
        signals.append("README is a project or module entry document")
        return _classification(
            path,
            DESIGN_DOC,
            "high",
            0.88,
            "README files describe project or module responsibilities and should not be treated as temporary notes.",
            signals,
        )

    if _is_artifact_path(parts, lower_path, lower_name):
        signals.append("path or filename looks like generated output")
        return _classification(
            path,
            ARTIFACT,
            "low",
            0.86,
            "File appears to be generated output or a sample artifact.",
            signals,
        )

    if _is_experiment_path(parts, lower_path, lower_name, sample):
        signals.append("path, filename, or content suggests experiment/prototype work")
        return _classification(
            path,
            EXPERIMENT,
            "low",
            0.84,
            "File looks like an experiment, prompt test, scratch file, or demo-only validation asset.",
            signals,
        )

    if _is_test_path(parts, lower_name):
        signals.append("path or filename follows test convention")
        return _classification(
            path,
            TEST_CODE,
            "high",
            0.9,
            "File follows formal test naming or lives under a test directory.",
            signals,
        )

    if _is_main_code_path(parts, file.extension):
        signals.append("file lives under source/package directory")
        return _classification(
            path,
            MAIN_CODE,
            "high",
            0.88,
            "File lives under a source package directory and is likely mainline code.",
            signals,
        )

    if _is_data_script(lower_path, lower_name, sample):
        signals.append("filename or content suggests data download/cleanup/conversion")
        return _classification(
            path,
            DATA_SCRIPT,
            "low",
            0.84,
            "File appears to support data download, cleanup, conversion, or migration.",
            signals,
        )

    if _is_dev_script(parts, lower_name, sample):
        signals.append("path, filename, or content suggests development automation")
        return _classification(
            path,
            DEV_SCRIPT,
            "medium",
            0.78,
            "File appears to be a development helper script.",
            signals,
        )

    if _is_todo(lower_name, sample):
        signals.append("filename or content contains todo/task-list markers")
        return _classification(
            path,
            TODO,
            "low",
            0.9,
            "File appears to be a todo or task tracking document.",
            signals,
        )

    if _is_research_doc(lower_path, lower_name, sample):
        signals.append("path, filename, or content suggests research notes")
        return _classification(
            path,
            RESEARCH_DOC,
            "low",
            0.82,
            "File appears to be research or investigation notes.",
            signals,
        )

    if _is_planning_doc(lower_path, lower_name, sample):
        signals.append("path, filename, or content suggests planning material")
        return _classification(
            path,
            PLANNING_DOC,
            "medium",
            0.8,
            "File appears to describe project planning, roadmap, or phase notes.",
            signals,
        )

    if _is_design_doc(lower_path, lower_name, sample):
        signals.append("path, filename, or content suggests design documentation")
        return _classification(
            path,
            DESIGN_DOC,
            "medium",
            0.78,
            "File appears to be design or architecture documentation.",
            signals,
        )

    return _classification(
        path,
        UNKNOWN,
        "unknown",
        0.35,
        "No strong hygiene classification signals were found.",
        ["no strong classification signal"],
    )


def _classification(
    path: str,
    category: str,
    relevance: str,
    confidence: float,
    reason: str,
    signals: list[str],
) -> FileClassification:
    return FileClassification(
        path=path,
        category=category,
        mainline_relevance=relevance,
        confidence=confidence,
        reason=reason,
        signals=signals,
    )


def _is_readme(name: str) -> bool:
    return name.lower() == "readme.md"


def _is_main_code_path(parts: list[str], extension: str) -> bool:
    return extension == ".py" and bool(parts) and parts[0] in {"src", "lib", "app"}


def _is_test_path(parts: list[str], lower_name: str) -> bool:
    return (
        any(part in {"tests", "test"} for part in parts)
        or lower_name.startswith("test_")
        or lower_name.endswith("_test.py")
    )


def _is_experiment_path(
    parts: list[str],
    lower_path: str,
    lower_name: str,
    sample: str,
) -> bool:
    experiment_markers = (
        "experiment",
        "experiments",
        "scratch",
        "prototype",
        "prompt",
        "playground",
        "demo_only",
        "tmp_",
        "temp_",
    )
    return (
        any(part in {"experiments", "notebooks", "playground"} for part in parts)
        or any(marker in lower_name for marker in experiment_markers)
        or any(marker in lower_path for marker in ("/scratch", "/tmp", "/temp"))
        or "prompt experiment" in sample
        or "demo-only" in sample
    )


def _is_data_script(lower_path: str, lower_name: str, sample: str) -> bool:
    name_markers = ("download", "fetch", "clean", "etl", "migrate", "seed")
    content_markers = ("pandas", "read_csv", "to_csv", "requests.get", "dataset")
    return (
        any(marker in lower_name for marker in name_markers)
        or "/data/" in lower_path
        or any(marker in sample for marker in content_markers)
    )


def _is_dev_script(parts: list[str], lower_name: str, sample: str) -> bool:
    name_markers = ("bootstrap", "setup", "release", "build", "lint", "format")
    return (
        (parts and parts[0] == "scripts")
        or any(marker in lower_name for marker in name_markers)
        or "subprocess.run" in sample
    )


def _is_todo(lower_name: str, sample: str) -> bool:
    return lower_name in {"todo.md", "todos.md"} or lower_name.startswith("todo") or "- [ ]" in sample


def _is_research_doc(lower_path: str, lower_name: str, sample: str) -> bool:
    return (
        "research" in lower_path
        or "investigation" in lower_name
        or "benchmark notes" in sample
        or "references" in sample
    )


def _is_planning_doc(lower_path: str, lower_name: str, sample: str) -> bool:
    return (
        "planning" in lower_path
        or "roadmap" in lower_name
        or "plan" in lower_name
        or "phase " in sample
    )


def _is_design_doc(lower_path: str, lower_name: str, sample: str) -> bool:
    return (
        "design" in lower_path
        or "architecture" in lower_name
        or "方案" in sample
        or "architecture" in sample
    )


def _is_artifact_path(parts: list[str], lower_path: str, lower_name: str) -> bool:
    artifact_dirs = {"outputs", "output", "artifacts", "reports"}
    artifact_markers = ("report", "result", "sample", "snapshot")
    return (
        any(part in artifact_dirs for part in parts)
        or any(marker in lower_name for marker in artifact_markers)
        and lower_path.endswith((".json", ".md", ".txt"))
    )


def classify_files_semantic(
    repo_path: Path | str,
    scanned_files: list[ScannedFile],
    llm_classifier: LLMClassifier,
    *,
    folder_summaries: dict[str, Any] | None = None,
) -> tuple[list[FileClassification], list[SemanticClassification]]:
    """Classify files using rules first, then LLM for non-protected files.

    Flow
    ----
    1. Run rule-based :func:`classify_files` on all files.
    2. Collect evidence (imports, reverse imports, test refs, config decls).
    3. Skip files where the safety guard is triggered (mainline/protected).
    4. Run LLM on the remaining candidates.
    5. Return both classification lists.

    Parameters
    ----------
    repo_path:
        Root of the repository.
    scanned_files:
        Output of :func:`~code_review_agent.hygiene.scanner.scan_repository`.
    llm_classifier:
        Any object satisfying the :class:`~code_review_agent.hygiene.llm_classifier.LLMClassifier`
        protocol.  Use :class:`~code_review_agent.hygiene.llm_classifier.FakeLLMClassifier`
        for tests and CI runs without a real LLM API key.
    folder_summaries:
        Optional parsed ``folder_summaries.json`` for extra folder context.

    Returns
    -------
    tuple[list[FileClassification], list[SemanticClassification]]
        Rule-based classifications (all files) and semantic classifications
        (non-protected, non-mainline files only).
    """
    rule_classifications = classify_files(repo_path, scanned_files)
    rule_by_path = {c.path: c for c in rule_classifications}

    evidence_list = collect_evidence(
        repo_path, scanned_files, folder_summaries=folder_summaries
    )

    # Only send non-protected, non-mainline files to the LLM.
    candidates = [
        ev for ev in evidence_list
        if not is_safety_guard_triggered(ev)
        and rule_by_path.get(ev.path, FileClassification(
            path=ev.path, category="unknown", mainline_relevance="unknown",
            confidence=0.0, reason="", signals=[]
        )).mainline_relevance != "high"
    ]

    semantic_classifications = classify_with_llm(candidates, llm_classifier)
    return rule_classifications, semantic_classifications


def _find_imported_local_python_paths(
    repo_path: Path,
    scanned_files: list[ScannedFile],
) -> set[str]:
    python_files = [file for file in scanned_files if file.extension == ".py"]
    module_to_path = build_module_path_index(python_files)
    imported: set[str] = set()

    import ast as _ast
    for file in python_files:
        try:
            tree = _ast.parse(file.content_sample)
        except SyntaxError:
            continue
        for node in _ast.walk(tree):
            module_names = extract_import_names(node)
            for module_name in module_names:
                candidate = resolve_import(module_name, module_to_path)
                if candidate and candidate != file.path:
                    imported.add(candidate)

    return imported
