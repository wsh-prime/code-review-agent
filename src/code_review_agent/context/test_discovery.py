"""Lightweight related-test discovery for RepoMap."""

from __future__ import annotations

from pathlib import Path

from code_review_agent.models import PythonModuleSummary


def discover_related_tests(
    repo_path: Path | str,
    python_paths: list[str],
    module_summaries: list[PythonModuleSummary] | None = None,
) -> dict[str, list[str]]:
    """Map source Python files to tests that appear to exercise them.

    This intentionally stays conservative and cheap: path naming conventions
    first, then simple import/symbol-name references in test files.
    """

    root = Path(repo_path).resolve()
    summaries_by_path = {
        summary.path: summary for summary in module_summaries or []
    }
    test_paths = [path for path in python_paths if _is_test_path(path)]
    related: dict[str, list[str]] = {}

    for source_path in python_paths:
        if _is_test_path(source_path):
            continue

        matches: set[str] = set()
        source_stem = Path(source_path).stem
        import_names = _module_import_names(source_path)
        symbol_names = _symbol_names(summaries_by_path.get(source_path))

        for test_path in test_paths:
            test_stem = Path(test_path).stem
            if _path_name_matches(source_stem, test_stem):
                matches.add(test_path)
                continue

            text = _read_text(root / test_path)
            if any(import_name in text for import_name in import_names):
                matches.add(test_path)
                continue

            if symbol_names and any(symbol_name in text for symbol_name in symbol_names):
                matches.add(test_path)

        related[source_path] = sorted(matches)

    return related


def _is_test_path(path: str) -> bool:
    parts = Path(path).parts
    name = Path(path).name
    return (
        "tests" in parts
        or name.startswith("test_")
        or name.endswith("_test.py")
    )


def _path_name_matches(source_stem: str, test_stem: str) -> bool:
    return test_stem in {f"test_{source_stem}", f"{source_stem}_test"}


def _module_import_names(path: str) -> set[str]:
    module_name = Path(path).with_suffix("").as_posix().replace("/", ".")
    names = {module_name}
    if module_name.startswith("src."):
        names.add(module_name.removeprefix("src."))
    return names


def _symbol_names(summary: PythonModuleSummary | None) -> set[str]:
    if summary is None:
        return set()

    return {
        symbol.name
        for symbol in [*summary.classes, *summary.functions, *summary.methods]
        if not symbol.name.startswith("_")
    }


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
