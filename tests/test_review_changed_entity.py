from __future__ import annotations

from pathlib import Path

from code_review_agent.context.repo_map import build_repo_map
from code_review_agent.review.changed_entity import extract_changed_entities
from code_review_agent.review.diff_parser import parse_unified_diff


def test_maps_hunk_to_function_method_class_and_module(tmp_path: Path) -> None:
    _write_repo(tmp_path)
    repo_map = build_repo_map(tmp_path)
    diff_text = """diff --git a/src/shop/service.py b/src/shop/service.py
--- a/src/shop/service.py
+++ b/src/shop/service.py
@@ -1,8 +1,10 @@
 from dataclasses import dataclass
+MAX_ITEMS = 10
 
 class OrderService:
+    channel = "web"
     def create(self, name: str) -> str:
-        return normalize_name(name)
+        return normalize_name(name)[:MAX_ITEMS]
 
 def normalize_name(name: str) -> str:
-    return name.strip().lower()
+    return name.strip().lower().replace(" ", "-")
"""

    changes = parse_unified_diff(diff_text)
    entities = extract_changed_entities(changes, repo_map)

    by_type = {(entity.entity_type, entity.qualified_name) for entity in entities}
    assert ("module", "src.shop.service") in by_type
    assert ("class", "OrderService") in by_type
    assert ("method", "OrderService.create") in by_type
    assert ("function", "normalize_name") in by_type
    assert all(entity.hunk_ids for entity in entities)


def test_falls_back_to_module_for_unmapped_or_deleted_file(tmp_path: Path) -> None:
    _write_repo(tmp_path)
    repo_map = build_repo_map(tmp_path)
    diff_text = """diff --git a/src/shop/missing.py b/src/shop/missing.py
deleted file mode 100644
--- a/src/shop/missing.py
+++ /dev/null
@@ -1,2 +0,0 @@
-VALUE = 1
-print(VALUE)
"""

    changes = parse_unified_diff(diff_text)
    entities = extract_changed_entities(changes, repo_map)

    assert len(entities) == 1
    assert entities[0].entity_type == "module"
    assert entities[0].path == "src/shop/missing.py"
    assert entities[0].hunk_ids == ["src/shop/missing.py:1"]


def _write_repo(root: Path) -> None:
    (root / "src" / "shop").mkdir(parents=True)
    (root / "src" / "shop" / "service.py").write_text(
        "from dataclasses import dataclass\n"
        "MAX_ITEMS = 10\n"
        "\n"
        "class OrderService:\n"
        '    channel = "web"\n'
        "    def create(self, name: str) -> str:\n"
        "        return normalize_name(name)[:MAX_ITEMS]\n"
        "\n"
        "def normalize_name(name: str) -> str:\n"
        '    return name.strip().lower().replace(" ", "-")\n',
        encoding="utf-8",
    )
