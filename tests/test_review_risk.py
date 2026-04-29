from __future__ import annotations

from pathlib import Path

from code_review_agent.context.repo_map import build_repo_map
from code_review_agent.hygiene.classifier import EXPERIMENT
from code_review_agent.models import FileClassification
from code_review_agent.review.changed_entity import extract_changed_entities
from code_review_agent.review.diff_parser import parse_unified_diff
from code_review_agent.review.risk import (
    API_CHANGE,
    BEHAVIOR_CHANGE,
    CONFIG_CHANGE,
    DEPENDENCY_CHANGE,
    DESIGN_CONSTRAINT_VIOLATION,
    DOC_ONLY,
    ERROR_HANDLING_CHANGE,
    EXPERIMENT_ARTIFACT,
    SECURITY_SENSITIVE,
    TEST_GAP,
    classify_risks,
)


def test_test_gap_triggers_when_related_tests_are_not_changed(tmp_path: Path) -> None:
    _write_order_repo(tmp_path)
    repo_map = build_repo_map(tmp_path)
    changes = parse_unified_diff(
        """diff --git a/src/shop/service.py b/src/shop/service.py
--- a/src/shop/service.py
+++ b/src/shop/service.py
@@ -1,4 +1,4 @@
 def create_order(total: int) -> bool:
     if total <= 0:
         return False
-    return True
+    return total > 10
"""
    )
    entities = extract_changed_entities(changes, repo_map)

    signals = classify_risks(changes, repo_map, entities)
    tags = {signal.tag for signal in signals}

    assert TEST_GAP in tags
    assert BEHAVIOR_CHANGE in tags
    test_gap = next(signal for signal in signals if signal.tag == TEST_GAP)
    assert "test_discovery:tests/test_service.py" in test_gap.evidence_ids
    assert any(evidence_id.startswith("diff:src/shop/service.py") for evidence_id in test_gap.evidence_ids)


def test_doc_only_patch_returns_only_doc_only_risk(tmp_path: Path) -> None:
    _write_order_repo(tmp_path)
    repo_map = build_repo_map(tmp_path)
    changes = parse_unified_diff(
        """diff --git a/docs/design.md b/docs/design.md
--- a/docs/design.md
+++ b/docs/design.md
@@ -1 +1,2 @@
 # Design
+More notes.
"""
    )

    signals = classify_risks(changes, repo_map, [])

    assert [signal.tag for signal in signals] == [DOC_ONLY]


def test_design_constraint_triggers_only_when_baseline_is_reliable(
    tmp_path: Path,
) -> None:
    _write_docstring_baseline_repo(tmp_path)
    repo_map = build_repo_map(tmp_path)
    changes = parse_unified_diff(
        """diff --git a/src/shop/service.py b/src/shop/service.py
--- a/src/shop/service.py
+++ b/src/shop/service.py
@@ -17,2 +17,2 @@ def changed_feature() -> str:
 def changed_feature() -> str:
-    return "old"
+    return "new"
"""
    )
    entities = extract_changed_entities(changes, repo_map)

    signals = classify_risks(changes, repo_map, entities)

    assert repo_map.style_baseline is not None
    assert repo_map.style_baseline.total_public_functions >= 5
    assert any(signal.tag == DESIGN_CONSTRAINT_VIOLATION for signal in signals)


def test_design_constraint_skips_small_style_samples(tmp_path: Path) -> None:
    _write_order_repo(tmp_path)
    repo_map = build_repo_map(tmp_path)
    changes = parse_unified_diff(
        """diff --git a/src/shop/service.py b/src/shop/service.py
--- a/src/shop/service.py
+++ b/src/shop/service.py
@@ -1,4 +1,4 @@
 def create_order(total: int) -> bool:
     if total <= 0:
         return False
-    return True
+    return total > 10
"""
    )
    entities = extract_changed_entities(changes, repo_map)

    signals = classify_risks(changes, repo_map, entities)

    assert all(signal.tag != DESIGN_CONSTRAINT_VIOLATION for signal in signals)


def test_risk_classifier_detects_config_dependency_error_security_and_api(
    tmp_path: Path,
) -> None:
    _write_order_repo(tmp_path)
    repo_map = build_repo_map(tmp_path)
    changes = parse_unified_diff(
        """diff --git a/pyproject.toml b/pyproject.toml
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -1,2 +1,3 @@
 [project]
 dependencies = []
+dependencies = ["requests"]
diff --git a/src/shop/service.py b/src/shop/service.py
--- a/src/shop/service.py
+++ b/src/shop/service.py
@@ -1,4 +1,8 @@
-def create_order(total: int) -> bool:
+def create_order(total: int, token: str | None = None) -> bool:
     if total <= 0:
-        return False
+        raise ValueError("invalid")
+    try:
+        return bool(token) or total > 10
+    except Exception:
+        return False
     return True
"""
    )
    entities = extract_changed_entities(changes, repo_map)

    signals = classify_risks(changes, repo_map, entities)
    tags = {signal.tag for signal in signals}

    assert CONFIG_CHANGE in tags
    assert DEPENDENCY_CHANGE in tags
    assert API_CHANGE in tags
    assert ERROR_HANDLING_CHANGE in tags
    assert SECURITY_SENSITIVE in tags


def test_experiment_artifact_uses_path_or_hygiene_classification(
    tmp_path: Path,
) -> None:
    _write_order_repo(tmp_path)
    repo_map = build_repo_map(tmp_path)
    changes = parse_unified_diff(
        """diff --git a/src/shop/debug_flow.py b/src/shop/debug_flow.py
new file mode 100644
--- /dev/null
+++ b/src/shop/debug_flow.py
@@ -0,0 +1,2 @@
+def run():
+    return None
"""
    )
    hygiene = [
        FileClassification(
            path="src/shop/debug_flow.py",
            category=EXPERIMENT,
            mainline_relevance="low",
            confidence=0.84,
            reason="Debug helper.",
        )
    ]

    signals = classify_risks(
        changes,
        repo_map,
        [],
        hygiene_classifications=hygiene,
    )
    artifact = next(signal for signal in signals if signal.tag == EXPERIMENT_ARTIFACT)

    assert "hygiene:src/shop/debug_flow.py" in artifact.evidence_ids


def _write_order_repo(root: Path) -> None:
    (root / "src" / "shop").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "docs").mkdir()
    (root / "src" / "shop" / "service.py").write_text(
        "def create_order(total: int) -> bool:\n"
        "    if total <= 0:\n"
        "        return False\n"
        "    return total > 10\n",
        encoding="utf-8",
    )
    (root / "tests" / "test_service.py").write_text(
        "from shop.service import create_order\n\n"
        "def test_create_order():\n"
        "    assert create_order(20)\n",
        encoding="utf-8",
    )


def _write_docstring_baseline_repo(root: Path) -> None:
    (root / "src" / "shop").mkdir(parents=True)
    (root / "src" / "shop" / "service.py").write_text(
        'def documented_one() -> int:\n    """Doc."""\n    return 1\n\n'
        'def documented_two() -> int:\n    """Doc."""\n    return 2\n\n'
        'def documented_three() -> int:\n    """Doc."""\n    return 3\n\n'
        'def documented_four() -> int:\n    """Doc."""\n    return 4\n\n'
        "def changed_feature() -> str:\n"
        '    return "new"\n',
        encoding="utf-8",
    )
