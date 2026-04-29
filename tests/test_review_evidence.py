from __future__ import annotations

import json
from pathlib import Path

from code_review_agent.context.repo_map import build_repo_map
from code_review_agent.hygiene.classifier import EXPERIMENT
from code_review_agent.models import FileClassification, RiskSignal
from code_review_agent.review.changed_entity import extract_changed_entities
from code_review_agent.review.diff_parser import parse_unified_diff
from code_review_agent.review.evidence import (
    build_evidence_package,
    find_missing_evidence_ids,
)
from code_review_agent.review.risk import (
    EXPERIMENT_ARTIFACT,
    TEST_GAP,
    classify_risks,
    diff_evidence_id,
)


def test_build_evidence_package_indexes_diff_entity_risk_and_tests(
    tmp_path: Path,
) -> None:
    _write_repo(tmp_path)
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
    risks = classify_risks(changes, repo_map, entities)

    package = build_evidence_package(tmp_path, changes, entities, risks, repo_map)

    assert package.repo_root == str(tmp_path.resolve())
    assert "diff:src/shop/service.py:4" in package.evidence_index
    assert "entity:src/shop/service.py:create_order" in package.evidence_index
    assert "test_discovery:tests/test_service.py" in package.evidence_index
    assert any(
        evidence_id.startswith(f"risk:{TEST_GAP}:src/shop/service.py")
        for evidence_id in package.evidence_index
    )
    assert find_missing_evidence_ids(package) == []
    json.dumps(package.to_dict())


def test_evidence_package_includes_hygiene_and_redaction_metadata(
    tmp_path: Path,
) -> None:
    _write_repo(tmp_path)
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
    risks = classify_risks(
        changes,
        repo_map,
        [],
        hygiene_classifications=hygiene,
    )

    package = build_evidence_package(
        tmp_path,
        changes,
        [],
        risks,
        repo_map,
        hygiene_classifications=hygiene,
    )

    assert "hygiene:src/shop/debug_flow.py" in package.evidence_index
    assert any(signal.tag == EXPERIMENT_ARTIFACT for signal in package.risk_signals)
    assert "commit_message" in package.metadata["redacted"]
    assert package.metadata["target_repo_modified"] is False


def test_find_missing_evidence_ids_reports_invalid_references(
    tmp_path: Path,
) -> None:
    repo_map = build_repo_map(tmp_path)
    invalid = RiskSignal(
        tag=TEST_GAP,
        confidence=0.5,
        reason="Bad reference for filter tests.",
        evidence_ids=[diff_evidence_id("src/missing.py", 99)],
    )

    package = build_evidence_package(tmp_path, [], [], [invalid], repo_map)

    assert find_missing_evidence_ids(package) == ["diff:src/missing.py:99"]


def _write_repo(root: Path) -> None:
    (root / "src" / "shop").mkdir(parents=True)
    (root / "tests").mkdir()
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
