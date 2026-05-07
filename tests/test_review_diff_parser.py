from __future__ import annotations

import logging
from pathlib import Path

import pytest

from code_review_agent.review.diff_parser import DiffParseError, parse_unified_diff


def test_parse_demo_patch_preserves_hunk_line_numbers() -> None:
    project_root = Path(__file__).resolve().parents[1]
    diff_text = (project_root / "examples" / "demo_repo" / "demo.patch").read_text(
        encoding="utf-8"
    )

    changes = parse_unified_diff(diff_text)

    assert len(changes) == 1
    change = changes[0]
    assert change.old_path == "src/shop/service.py"
    assert change.new_path == "src/shop/service.py"
    assert change.change_type == "modified"
    assert len(change.hunks) == 1

    hunk = change.hunks[0]
    assert hunk.old_start == 16
    assert hunk.old_count == 5
    assert hunk.new_start == 16
    assert hunk.new_count == 5
    assert hunk.lines[0].line_type == "context"
    assert hunk.lines[0].old_lineno == 16
    assert hunk.lines[0].new_lineno == 16

    added = [line for line in hunk.lines if line.line_type == "added"]
    assert len(added) == 1
    assert added[0].old_lineno is None
    assert added[0].new_lineno == 18
    assert "10_000" in added[0].content


def test_parse_added_deleted_and_renamed_files() -> None:
    diff_text = """diff --git a/new.py b/new.py
new file mode 100644
index 0000000..1111111
--- /dev/null
+++ b/new.py
@@ -0,0 +1,2 @@
+print("hi")
+
diff --git a/old.py b/old.py
deleted file mode 100644
index 2222222..0000000
--- a/old.py
+++ /dev/null
@@ -1,2 +0,0 @@
-print("bye")
-
diff --git a/old_name.py b/new_name.py
similarity index 100%
rename from old_name.py
rename to new_name.py
"""

    changes = parse_unified_diff(diff_text)

    assert [change.change_type for change in changes] == [
        "added",
        "deleted",
        "renamed",
    ]
    assert changes[0].old_path is None
    assert changes[0].new_path == "new.py"
    assert changes[0].hunks[0].lines[0].new_lineno == 1
    assert changes[1].old_path == "old.py"
    assert changes[1].new_path is None
    assert changes[1].hunks[0].lines[0].old_lineno == 1
    assert changes[2].old_path == "old_name.py"
    assert changes[2].new_path == "new_name.py"
    assert changes[2].hunks == []


def test_parse_binary_file_records_change_without_hunks() -> None:
    diff_text = """diff --git a/image.png b/image.png
new file mode 100644
index 0000000..1111111
Binary files /dev/null and b/image.png differ
"""

    changes = parse_unified_diff(diff_text)

    assert len(changes) == 1
    assert changes[0].change_type == "added"
    assert changes[0].old_path is None
    assert changes[0].new_path == "image.png"
    assert changes[0].hunks == []


def test_empty_diff_raises_clear_error() -> None:
    with pytest.raises(DiffParseError, match="Diff is empty"):
        parse_unified_diff("\n  \n")


def test_malformed_hunk_is_skipped_with_warning(caplog: pytest.LogCaptureFixture) -> None:
    diff_text = """diff --git a/src/app.py b/src/app.py
--- a/src/app.py
+++ b/src/app.py
@@ malformed hunk
+broken
"""

    with caplog.at_level(logging.WARNING):
        changes = parse_unified_diff(diff_text)

    assert len(changes) == 1
    assert changes[0].hunks == []
    assert "Skipping malformed hunk header" in caplog.text
