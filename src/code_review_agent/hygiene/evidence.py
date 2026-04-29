"""Evidence collection for semantic hygiene classification.

Gathers all available signals for each file in a repository: imports,
reverse-import graph, test references, config declarations and optional
folder-level context from a prior ``summary`` run.

This module also owns the shared AST utility helpers that ``classifier.py``
previously duplicated internally.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from code_review_agent.hygiene.scanner import ScannedFile
from code_review_agent.models import HygieneEvidence


# Files whose mere presence in the scanned list activates the safety guard for
# anything they reference.
_CONFIG_FILENAMES: frozenset[str] = frozenset(
    {
        "pyproject.toml",
        "setup.cfg",
        "setup.py",
        "tox.ini",
        ".flake8",
        "Makefile",
        "requirements.txt",
        "requirements-dev.txt",
    }
)

# Files that are always mainline and must never get a move suggestion.
_CORE_FILENAMES: frozenset[str] = frozenset(
    {
        "readme.md",
        "license",
        "license.md",
        "license.txt",
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        ".gitignore",
    }
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def collect_evidence(
    repo_path: Path | str,
    scanned_files: list[ScannedFile],
    *,
    folder_summaries: dict[str, Any] | None = None,
) -> list[HygieneEvidence]:
    """Return one :class:`HygieneEvidence` per scanned file.

    Parameters
    ----------
    repo_path:
        Root of the repository (used to resolve config declarations).
    scanned_files:
        Output of :func:`~code_review_agent.hygiene.scanner.scan_repository`.
    folder_summaries:
        Optional parsed ``folder_summaries.json`` produced by the ``summary``
        command.  Expected shape::

            { "src/orders": {"responsibility": "...", ...}, ... }
    """
    python_files = [f for f in scanned_files if f.extension == ".py"]
    module_to_path = build_module_path_index(python_files)

    # --- reverse-import graph -------------------------------------------------
    imported_by: dict[str, list[str]] = {f.path: [] for f in scanned_files}
    for file in python_files:
        for module_name in _parse_imports(file):
            candidate = resolve_import(module_name, module_to_path)
            if candidate and candidate != file.path:
                imported_by.setdefault(candidate, []).append(file.path)

    # --- test-reference graph -------------------------------------------------
    test_paths = {f.path for f in scanned_files if _is_test_file(f.path)}
    referenced_by_tests: dict[str, list[str]] = {f.path: [] for f in scanned_files}
    for file in scanned_files:
        if file.path not in test_paths:
            continue
        for module_name in _parse_imports(file):
            candidate = resolve_import(module_name, module_to_path)
            if candidate and candidate != file.path:
                referenced_by_tests.setdefault(candidate, []).append(file.path)

    # --- config declarations --------------------------------------------------
    config_files = [f for f in scanned_files if _is_config_file(f.path)]
    declared_in_config: dict[str, list[str]] = {}
    for cfg in config_files:
        for file in scanned_files:
            stem = Path(file.path).stem
            if stem in cfg.content_sample or file.path in cfg.content_sample:
                declared_in_config.setdefault(file.path, []).append(cfg.path)

    # --- per-file imports -----------------------------------------------------
    file_imports: dict[str, list[str]] = {}
    for file in python_files:
        file_imports[file.path] = _parse_imports(file)

    # --- assemble HygieneEvidence objects -------------------------------------
    evidences: list[HygieneEvidence] = []
    for file in scanned_files:
        folder = str(Path(file.path).parent)
        folder_context: str | None = None
        if folder_summaries:
            entry = folder_summaries.get(folder) or folder_summaries.get(folder.replace("\\", "/"))
            if entry and isinstance(entry, dict):
                folder_context = entry.get("responsibility")

        signals = _collect_signals(
            file,
            imported_by=imported_by,
            referenced_by_tests=referenced_by_tests,
            declared_in_config=declared_in_config,
        )

        evidences.append(
            HygieneEvidence(
                path=file.path,
                content_sample=file.content_sample[:500],
                imports=file_imports.get(file.path, []),
                imported_by=imported_by.get(file.path, []),
                referenced_by_tests=referenced_by_tests.get(file.path, []),
                declared_in_config=declared_in_config.get(file.path, []),
                folder_context=folder_context,
                previous_role=None,
                signals=signals,
            )
        )

    return evidences


def is_safety_guard_triggered(evidence: HygieneEvidence) -> bool:
    """Return True if the file must not receive a move suggestion.

    Triggers:
    - Another local module imports it.
    - A formal test file imports it.
    - A config file declares it.
    - It is a core project file (README, LICENSE, pyproject.toml, …).
    """
    if evidence.imported_by:
        return True
    if evidence.referenced_by_tests:
        return True
    if evidence.declared_in_config:
        return True
    if Path(evidence.path).name.lower() in _CORE_FILENAMES:
        return True
    return False


# ---------------------------------------------------------------------------
# Shared AST utilities (also used by classifier.py)
# ---------------------------------------------------------------------------


def build_module_path_index(python_files: list[ScannedFile]) -> dict[str, str]:
    """Map importable module names → relative file paths."""
    index: dict[str, str] = {}
    for file in python_files:
        path = Path(file.path)
        if path.name == "__init__.py":
            module = ".".join(path.parent.parts)
        else:
            module = ".".join(path.with_suffix("").parts)
        if module.startswith("src."):
            index[module[4:]] = file.path
        index[module] = file.path
    return index


def resolve_import(module_name: str, module_to_path: dict[str, str]) -> str | None:
    """Resolve an import statement to a local file path, or None."""
    parts = module_name.split(".")
    for end in range(len(parts), 0, -1):
        candidate = ".".join(parts[:end])
        if candidate in module_to_path:
            return module_to_path[candidate]
    return None


def extract_import_names(node: ast.AST) -> list[str]:
    """Return top-level module names referenced by an import AST node."""
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    if isinstance(node, ast.ImportFrom) and node.module:
        return [node.module]
    return []


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _parse_imports(file: ScannedFile) -> list[str]:
    """Parse import names from a file's content sample. Returns [] on error."""
    try:
        tree = ast.parse(file.content_sample)
    except (SyntaxError, ValueError):
        return []
    names: list[str] = []
    for node in ast.walk(tree):
        names.extend(extract_import_names(node))
    return names


def _is_test_file(path: str) -> bool:
    parts = path.split("/")
    lower_name = parts[-1].lower()
    return (
        any(part in {"tests", "test"} for part in parts)
        or lower_name.startswith("test_")
        or lower_name.endswith("_test.py")
    )


def _is_config_file(path: str) -> bool:
    return Path(path).name.lower() in _CONFIG_FILENAMES


def _collect_signals(
    file: ScannedFile,
    *,
    imported_by: dict[str, list[str]],
    referenced_by_tests: dict[str, list[str]],
    declared_in_config: dict[str, list[str]],
) -> list[str]:
    signals: list[str] = []
    if imported_by.get(file.path):
        signals.append(f"imported by: {', '.join(imported_by[file.path])}")
    if referenced_by_tests.get(file.path):
        signals.append(f"referenced by tests: {', '.join(referenced_by_tests[file.path])}")
    if declared_in_config.get(file.path):
        signals.append(f"declared in config: {', '.join(declared_in_config[file.path])}")
    if _is_test_file(file.path):
        signals.append("file is a formal test")
    if Path(file.path).name.lower() in _CORE_FILENAMES:
        signals.append("file is a core project file")
    return signals
