from __future__ import annotations

from pathlib import Path

from code_review_agent.context.repo_map import build_repo_map
from code_review_agent.hygiene.classifier import EXPERIMENT
from code_review_agent.models import FileClassification
from code_review_agent.review.changed_entity import extract_changed_entities
from code_review_agent.review.diff_parser import parse_unified_diff
from code_review_agent.review.evidence import build_evidence_package
from code_review_agent.review.risk import (
    DEPENDENCY_CHANGE,
    DOC_ONLY,
    ERROR_HANDLING_CHANGE,
    EXPERIMENT_ARTIFACT,
    TEST_GAP,
    classify_risks,
)
from code_review_agent.review.rules import run_rules


def test_rules_create_test_gap_finding(tmp_path: Path) -> None:
    _write_repo(tmp_path)
    package = _package_for_diff(
        tmp_path,
        """diff --git a/src/shop/service.py b/src/shop/service.py
--- a/src/shop/service.py
+++ b/src/shop/service.py
@@ -1,4 +1,4 @@
 def create_order(total: int) -> bool:
     if total <= 0:
         return False
-    return True
+    return total > 10
""",
    )

    result = run_rules(package)

    assert [issue.category for issue in result.findings] == [TEST_GAP]
    assert result.findings[0].severity == "medium"
    assert result.findings[0].evidence_ids
    assert result.needs_human_review == []


def test_rules_create_experiment_artifact_finding(tmp_path: Path) -> None:
    _write_repo(tmp_path)
    hygiene = [
        FileClassification(
            path="src/shop/debug_flow.py",
            category=EXPERIMENT,
            mainline_relevance="low",
            confidence=0.84,
            reason="Debug helper.",
        )
    ]
    package = _package_for_diff(
        tmp_path,
        """diff --git a/src/shop/debug_flow.py b/src/shop/debug_flow.py
new file mode 100644
--- /dev/null
+++ b/src/shop/debug_flow.py
@@ -0,0 +1,2 @@
+def run():
+    return None
""",
        hygiene,
    )

    result = run_rules(package)

    assert [issue.category for issue in result.findings] == [EXPERIMENT_ARTIFACT]
    assert result.findings[0].file == "src/shop/debug_flow.py"


def test_rules_create_broad_exception_finding(tmp_path: Path) -> None:
    _write_repo(tmp_path)
    package = _package_for_diff(
        tmp_path,
        """diff --git a/src/shop/service.py b/src/shop/service.py
--- a/src/shop/service.py
+++ b/src/shop/service.py
@@ -1,4 +1,8 @@
 def create_order(total: int) -> bool:
+    try:
+        return total > 10
+    except Exception:
+        return False
     if total <= 0:
         return False
     return True
""",
    )

    result = run_rules(package)

    assert ERROR_HANDLING_CHANGE in {issue.category for issue in result.findings}


def test_rules_put_dependency_change_in_human_review(tmp_path: Path) -> None:
    _write_repo(tmp_path)
    package = _package_for_diff(
        tmp_path,
        """diff --git a/pyproject.toml b/pyproject.toml
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -1,2 +1,3 @@
 [project]
 dependencies = []
+dependencies = ["requests"]
""",
    )

    result = run_rules(package)

    assert result.findings == []
    assert [issue.category for issue in result.needs_human_review] == [
        DEPENDENCY_CHANGE
    ]


def test_rules_keep_doc_only_patch_silent(tmp_path: Path) -> None:
    _write_repo(tmp_path)
    package = _package_for_diff(
        tmp_path,
        """diff --git a/docs/design.md b/docs/design.md
--- a/docs/design.md
+++ b/docs/design.md
@@ -1 +1,2 @@
 # Design
+More notes.
""",
    )

    result = run_rules(package)

    assert [signal.tag for signal in package.risk_signals] == [DOC_ONLY]
    assert result.findings == []
    assert result.needs_human_review == []


def _package_for_diff(
    root: Path,
    diff_text: str,
    hygiene: list[FileClassification] | None = None,
):
    repo_map = build_repo_map(root)
    changes = parse_unified_diff(diff_text)
    entities = extract_changed_entities(changes, repo_map)
    risks = classify_risks(
        changes,
        repo_map,
        entities,
        hygiene_classifications=hygiene,
    )
    return build_evidence_package(
        root,
        changes,
        entities,
        risks,
        repo_map,
        hygiene_classifications=hygiene,
    )


def _write_repo(root: Path) -> None:
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
    (root / "pyproject.toml").write_text(
        "[project]\ndependencies = []\n",
        encoding="utf-8",
    )
