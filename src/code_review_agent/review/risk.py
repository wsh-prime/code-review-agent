"""Deterministic risk classification for parsed review diffs."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from code_review_agent.hygiene.classifier import PROCESS_CATEGORIES
from code_review_agent.models import (
    ChangedEntity,
    DiffFileChange,
    DiffHunk,
    DiffLine,
    FileClassification,
    RepoMap,
    RiskSignal,
)


API_CHANGE = "api_change"
BEHAVIOR_CHANGE = "behavior_change"
TEST_GAP = "test_gap"
CONFIG_CHANGE = "config_change"
DEPENDENCY_CHANGE = "dependency_change"
ERROR_HANDLING_CHANGE = "error_handling_change"
SECURITY_SENSITIVE = "security_sensitive"
DOC_ONLY = "doc_only"
EXPERIMENT_ARTIFACT = "experiment_artifact"
DESIGN_CONSTRAINT_VIOLATION = "design_constraint_violation"

CONFIG_PATHS = {
    "pyproject.toml",
    "setup.cfg",
    "setup.py",
    "tox.ini",
    "mypy.ini",
    ".pre-commit-config.yaml",
}
DEPENDENCY_FILES = {
    "requirements.txt",
    "requirements-dev.txt",
    "poetry.lock",
    "pdm.lock",
    "uv.lock",
    "package.json",
    "package-lock.json",
    "pyproject.toml",
}
SECURITY_TOKENS = (
    "auth",
    "token",
    "password",
    "passwd",
    "secret",
    "credential",
    "subprocess",
    "eval(",
    "exec(",
    "path",
)
EXPERIMENT_MARKERS = (
    "experiment",
    "experiments",
    "debug",
    "demo",
    "scratch",
    "tmp",
    "temp",
    "prototype",
    "playground",
    "generated",
)
SIGNATURE_RE = re.compile(r"^\s*(?:async\s+def|def|class)\s+([A-Za-z_][A-Za-z0-9_]*)")


def classify_risks(
    changes: list[DiffFileChange],
    repo_map: RepoMap,
    changed_entities: list[ChangedEntity],
    *,
    hygiene_classifications: list[FileClassification] | None = None,
) -> list[RiskSignal]:
    """Classify deterministic risk tags from diff and repository context."""

    if not changes:
        return []

    if _is_doc_only_patch(changes):
        changed_path = _change_path(changes[0]) or "patch"
        return [
            RiskSignal(
                tag=DOC_ONLY,
                confidence=0.95,
                reason="Patch only changes Markdown or docs paths.",
                evidence_ids=_first_diff_evidence_ids(changes) or [
                    diff_evidence_id(changed_path, 1)
                ],
            )
        ]

    hygiene_by_path = {
        classification.path: classification
        for classification in hygiene_classifications or []
    }
    signals: list[RiskSignal] = []

    signals.extend(_config_and_dependency_risks(changes))
    signals.extend(_api_change_risks(changes))
    signals.extend(_behavior_change_risks(changed_entities, changes))
    signals.extend(_test_gap_risks(changes, repo_map))
    signals.extend(_hunk_content_risks(changes))
    signals.extend(_experiment_artifact_risks(changes, hygiene_by_path))
    signals.extend(_design_constraint_risks(changes, repo_map, changed_entities))

    return _deduplicate_signals(signals)


def diff_evidence_id(path: str, line: int) -> str:
    return f"diff:{path}:{line}"


def entity_evidence_id(entity: ChangedEntity) -> str:
    return f"entity:{entity.path}:{entity.qualified_name}"


def risk_evidence_id(signal: RiskSignal) -> str:
    path = _path_from_evidence_ids(signal.evidence_ids) or "patch"
    return f"risk:{signal.tag}:{path}"


def test_discovery_evidence_id(path: str) -> str:
    return f"test_discovery:{path}"


def hygiene_evidence_id(path: str) -> str:
    return f"hygiene:{path}"


def _config_and_dependency_risks(changes: list[DiffFileChange]) -> list[RiskSignal]:
    signals: list[RiskSignal] = []
    for change in changes:
        path = _change_path(change)
        if path is None:
            continue
        if _is_config_path(path):
            signals.append(
                RiskSignal(
                    tag=CONFIG_CHANGE,
                    confidence=0.86,
                    reason=f"Configuration file changed: {path}.",
                    evidence_ids=_diff_ids_for_change(change),
                )
            )
        if _is_dependency_change(change):
            signals.append(
                RiskSignal(
                    tag=DEPENDENCY_CHANGE,
                    confidence=0.84,
                    reason=f"Dependency declaration changed: {path}.",
                    evidence_ids=_diff_ids_for_change(change),
                )
            )
    return signals


def _api_change_risks(changes: list[DiffFileChange]) -> list[RiskSignal]:
    signals: list[RiskSignal] = []
    for change in changes:
        path = _change_path(change)
        if path is None or not path.endswith(".py"):
            continue
        if Path(path).name == "__init__.py" and _has_added_or_removed_lines(change):
            signals.append(
                RiskSignal(
                    tag=API_CHANGE,
                    confidence=0.82,
                    reason=f"Package export module changed: {path}.",
                    evidence_ids=_diff_ids_for_change(change),
                )
            )
            continue

        signature_ids = [
            diff_evidence_id(path, _line_number(line))
            for hunk in change.hunks
            for line in hunk.lines
            if line.line_type in {"added", "removed"}
            and _is_public_signature_line(line.content)
        ]
        if signature_ids:
            signals.append(
                RiskSignal(
                    tag=API_CHANGE,
                    confidence=0.82,
                    reason=f"Public function or class signature changed in {path}.",
                    evidence_ids=signature_ids,
                )
            )
    return signals


def _behavior_change_risks(
    changed_entities: list[ChangedEntity], changes: list[DiffFileChange]
) -> list[RiskSignal]:
    changes_by_path = {
        path: change for change in changes if (path := _change_path(change)) is not None
    }
    signals: list[RiskSignal] = []

    for entity in changed_entities:
        if entity.entity_type not in {"function", "method"}:
            continue
        if _is_test_path(entity.path) or not entity.path.endswith(".py"):
            continue
        change = changes_by_path.get(entity.path)
        if change is None or not _has_logic_line_change(change):
            continue
        signals.append(
            RiskSignal(
                tag=BEHAVIOR_CHANGE,
                confidence=0.72,
                reason=f"Executable logic changed inside {entity.qualified_name}.",
                evidence_ids=[
                    entity_evidence_id(entity),
                    *_diff_ids_for_change(change),
                ],
            )
        )

    return signals


def _test_gap_risks(
    changes: list[DiffFileChange], repo_map: RepoMap
) -> list[RiskSignal]:
    changed_paths = {_change_path(change) for change in changes}
    changed_paths.discard(None)
    changed_test_paths = {path for path in changed_paths if _is_test_path(path)}
    signals: list[RiskSignal] = []

    for change in changes:
        path = _change_path(change)
        if (
            path is None
            or _is_test_path(path)
            or not path.endswith(".py")
            or not _has_added_or_removed_lines(change)
        ):
            continue

        related_tests = repo_map.related_tests.get(path, [])
        if not related_tests:
            continue
        if any(test_path in changed_test_paths for test_path in related_tests):
            continue

        signals.append(
            RiskSignal(
                tag=TEST_GAP,
                confidence=0.8,
                reason=(
                    f"{path} changed while related tests exist but were not "
                    "included in the patch."
                ),
                evidence_ids=[
                    *_diff_ids_for_change(change),
                    *[
                        test_discovery_evidence_id(test_path)
                        for test_path in related_tests
                    ],
                ],
            )
        )

    return signals


def _hunk_content_risks(changes: list[DiffFileChange]) -> list[RiskSignal]:
    signals: list[RiskSignal] = []
    for change in changes:
        path = _change_path(change)
        if path is None:
            continue
        diff_ids = _diff_ids_for_change(change)
        changed_text = "\n".join(
            line.content
            for hunk in change.hunks
            for line in hunk.lines
            if line.line_type in {"added", "removed"}
        )
        lower_text = changed_text.lower()

        if _has_error_handling_change(change):
            signals.append(
                RiskSignal(
                    tag=ERROR_HANDLING_CHANGE,
                    confidence=0.78,
                    reason=f"Error-handling control flow changed in {path}.",
                    evidence_ids=diff_ids,
                )
            )
        if any(token in lower_text for token in SECURITY_TOKENS):
            signals.append(
                RiskSignal(
                    tag=SECURITY_SENSITIVE,
                    confidence=0.74,
                    reason=f"Security-sensitive keywords changed in {path}.",
                    evidence_ids=diff_ids,
                )
            )

    return signals


def _experiment_artifact_risks(
    changes: list[DiffFileChange],
    hygiene_by_path: dict[str, FileClassification],
) -> list[RiskSignal]:
    signals: list[RiskSignal] = []
    for change in changes:
        path = change.new_path
        if path is None or change.change_type != "added":
            continue
        hygiene = hygiene_by_path.get(path)
        is_process_artifact = (
            hygiene is not None and hygiene.category in PROCESS_CATEGORIES
        )
        if not (_is_experiment_path(path) or is_process_artifact):
            continue
        evidence_ids = _diff_ids_for_change(change)
        if hygiene is not None:
            evidence_ids.append(hygiene_evidence_id(path))
        signals.append(
            RiskSignal(
                tag=EXPERIMENT_ARTIFACT,
                confidence=0.78,
                reason=f"New file looks like a process or experiment artifact: {path}.",
                evidence_ids=evidence_ids,
            )
        )
    return signals


def _design_constraint_risks(
    changes: list[DiffFileChange],
    repo_map: RepoMap,
    changed_entities: list[ChangedEntity],
) -> list[RiskSignal]:
    baseline = repo_map.style_baseline
    if baseline is None or baseline.total_public_functions < 5:
        return []

    signals: list[RiskSignal] = []
    if baseline.docstring_coverage_ratio >= 0.7:
        for entity in changed_entities:
            if (
                entity.entity_type not in {"function", "method"}
                or entity.name.startswith("_")
                or _is_test_path(entity.path)
                or _symbol_has_docstring(repo_map, entity)
            ):
                continue
            signals.append(
                RiskSignal(
                    tag=DESIGN_CONSTRAINT_VIOLATION,
                    confidence=0.72,
                    reason=(
                        f"Public {entity.entity_type} {entity.qualified_name} "
                        "lacks a docstring in a repository with high docstring coverage."
                    ),
                    evidence_ids=[entity_evidence_id(entity)],
                )
            )

    for change in changes:
        path = change.new_path
        if path is None or change.change_type != "added":
            continue
        if _new_test_name_violates_pattern(path, baseline.test_naming_pattern):
            signals.append(
                RiskSignal(
                    tag=DESIGN_CONSTRAINT_VIOLATION,
                    confidence=0.7,
                    reason=f"New test file does not follow {baseline.test_naming_pattern}: {path}.",
                    evidence_ids=_diff_ids_for_change(change),
                )
            )
        if _new_import_style_violates_baseline(change, baseline.dominant_import_style):
            signals.append(
                RiskSignal(
                    tag=DESIGN_CONSTRAINT_VIOLATION,
                    confidence=0.7,
                    reason=(
                        f"New import style differs from repository baseline "
                        f"({baseline.dominant_import_style}) in {path}."
                    ),
                    evidence_ids=_diff_ids_for_change(change),
                )
            )

    return signals


def _is_doc_only_patch(changes: list[DiffFileChange]) -> bool:
    paths = [_change_path(change) for change in changes]
    return bool(paths) and all(path is not None and _is_doc_path(path) for path in paths)


def _is_doc_path(path: str) -> bool:
    suffix = Path(path).suffix.lower()
    return path.startswith("docs/") or suffix in {".md", ".rst", ".txt"}


def _is_config_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    name = Path(normalized).name
    return (
        normalized.startswith(".github/workflows/")
        or name in CONFIG_PATHS
        or name.endswith((".ini", ".cfg", ".toml", ".yaml", ".yml"))
    )


def _is_dependency_change(change: DiffFileChange) -> bool:
    path = _change_path(change)
    if path is None:
        return False
    name = Path(path).name.lower()
    if name in DEPENDENCY_FILES or name.startswith("requirements"):
        if name == "pyproject.toml":
            return _changed_text_contains(change, ("dependencies", "requires"))
        return True
    return False


def _has_error_handling_change(change: DiffFileChange) -> bool:
    for hunk in change.hunks:
        for line in hunk.lines:
            if line.line_type not in {"added", "removed"}:
                continue
            text = line.content.strip()
            if text.startswith(("try:", "finally:")):
                return True
            if text.startswith("raise"):
                return True
            if text.startswith("except"):
                return True
    return False


def _has_logic_line_change(change: DiffFileChange) -> bool:
    for hunk in change.hunks:
        for line in hunk.lines:
            if line.line_type not in {"added", "removed"}:
                continue
            stripped = line.content.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith(("import ", "from ")):
                continue
            if _is_public_signature_line(line.content):
                continue
            return True
    return False


def _is_public_signature_line(content: str) -> bool:
    match = SIGNATURE_RE.match(content)
    return bool(match and not match.group(1).startswith("_"))


def _has_added_or_removed_lines(change: DiffFileChange) -> bool:
    return any(
        line.line_type in {"added", "removed"}
        for hunk in change.hunks
        for line in hunk.lines
    )


def _changed_text_contains(change: DiffFileChange, tokens: tuple[str, ...]) -> bool:
    lower_text = "\n".join(
        line.content.lower()
        for hunk in change.hunks
        for line in hunk.lines
        if line.line_type in {"added", "removed"}
    )
    return any(token in lower_text for token in tokens)


def _diff_ids_for_change(change: DiffFileChange) -> list[str]:
    path = _change_path(change)
    if path is None:
        return []
    ids: list[str] = []
    for hunk in change.hunks:
        for line in hunk.lines:
            if line.line_type not in {"added", "removed"}:
                continue
            ids.append(diff_evidence_id(path, _line_number(line)))
    if not ids:
        ids.append(diff_evidence_id(path, 1))
    return sorted(set(ids))


def _first_diff_evidence_ids(changes: list[DiffFileChange]) -> list[str]:
    ids: list[str] = []
    for change in changes:
        ids.extend(_diff_ids_for_change(change))
    return ids[:10]


def _line_number(line: DiffLine) -> int:
    return line.new_lineno or line.old_lineno or 1


def _change_path(change: DiffFileChange) -> str | None:
    return change.new_path or change.old_path


def _is_test_path(path: str) -> bool:
    parts = Path(path).parts
    name = Path(path).name
    return "tests" in parts or name.startswith("test_") or name.endswith("_test.py")


def _is_experiment_path(path: str) -> bool:
    normalized = path.replace("\\", "/").lower()
    parts = normalized.split("/")
    name = parts[-1]
    return (
        any(part in {"experiments", "playground", "tmp", "temp"} for part in parts)
        or any(marker in name for marker in EXPERIMENT_MARKERS)
    )


def _new_test_name_violates_pattern(path: str, pattern: str | None) -> bool:
    if pattern is None or not _is_test_path(path):
        return False
    name = Path(path).name
    if pattern == "test_*":
        return not name.startswith("test_")
    if pattern == "*_test":
        return not name.endswith("_test.py")
    return False


def _new_import_style_violates_baseline(
    change: DiffFileChange, dominant_import_style: str
) -> bool:
    if dominant_import_style == "mixed":
        return False
    for hunk in change.hunks:
        for line in hunk.lines:
            if line.line_type != "added":
                continue
            stripped = line.content.strip()
            if not stripped.startswith("from "):
                continue
            is_relative = stripped.startswith("from .")
            if dominant_import_style == "absolute" and is_relative:
                return True
            if dominant_import_style == "relative" and not is_relative:
                return True
    return False


def _symbol_has_docstring(repo_map: RepoMap, entity: ChangedEntity) -> bool:
    try:
        source = (Path(repo_map.root) / entity.path).read_text(
            encoding="utf-8", errors="replace"
        )
        tree = ast.parse(source)
    except (OSError, SyntaxError):
        return False

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if entity.entity_type == "function" and node.name == entity.name:
                return ast.get_docstring(node) is not None
        if isinstance(node, ast.ClassDef) and entity.entity_type == "method":
            class_name, _, method_name = entity.qualified_name.partition(".")
            if node.name != class_name:
                continue
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if child.name == method_name:
                        return ast.get_docstring(child) is not None
    return False


def _path_from_evidence_ids(evidence_ids: list[str]) -> str | None:
    for evidence_id in evidence_ids:
        parts = evidence_id.split(":")
        if len(parts) >= 2 and parts[0] in {"diff", "entity", "hygiene"}:
            return parts[1]
    return None


def _deduplicate_signals(signals: list[RiskSignal]) -> list[RiskSignal]:
    by_key: dict[tuple[str, tuple[str, ...]], RiskSignal] = {}
    for signal in signals:
        key = (signal.tag, tuple(sorted(signal.evidence_ids)))
        if key not in by_key:
            by_key[key] = signal
    return sorted(
        by_key.values(),
        key=lambda signal: (signal.tag, signal.reason, signal.evidence_ids),
    )
