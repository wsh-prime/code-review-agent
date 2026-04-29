"""Unified diff parser for the review pipeline."""

from __future__ import annotations

import logging
import re

from code_review_agent.models import DiffFileChange, DiffHunk, DiffLine


LOGGER = logging.getLogger(__name__)

HUNK_HEADER_RE = re.compile(
    r"^@@ -(?P<old_start>\d+)(?:,(?P<old_count>\d+))? "
    r"\+(?P<new_start>\d+)(?:,(?P<new_count>\d+))? @@"
    r"(?: (?P<section>.*))?$"
)


class DiffParseError(ValueError):
    """Raised when input is not a usable unified diff."""


def parse_unified_diff(diff_text: str) -> list[DiffFileChange]:
    """Parse unified diff text into structured file changes.

    Malformed hunks are skipped with a warning so one bad hunk does not hide
    the rest of a patch.
    """

    if not diff_text.strip():
        raise DiffParseError("Diff is empty; expected unified diff content.")

    lines = diff_text.splitlines()
    changes: list[DiffFileChange] = []
    current: DiffFileChange | None = None
    index = 0

    while index < len(lines):
        line = lines[index]

        if line.startswith("diff --git "):
            current = _start_file_change(line)
            changes.append(current)
            index += 1
            continue

        if current is None and line.startswith("--- "):
            current, index = _start_plain_file_change(lines, index)
            if current is not None:
                changes.append(current)
            continue

        if current is None:
            index += 1
            continue

        if line.startswith("new file mode"):
            current.change_type = "added"
            current.old_path = None
            index += 1
            continue

        if line.startswith("deleted file mode"):
            current.change_type = "deleted"
            current.new_path = None
            index += 1
            continue

        if line.startswith("rename from "):
            current.old_path = _clean_path(line.removeprefix("rename from "))
            current.change_type = "renamed"
            index += 1
            continue

        if line.startswith("rename to "):
            current.new_path = _clean_path(line.removeprefix("rename to "))
            current.change_type = "renamed"
            index += 1
            continue

        if line.startswith("Binary files ") or line == "GIT binary patch":
            _apply_binary_paths(current, line)
            index += 1
            continue

        if line.startswith("--- "):
            index = _apply_file_headers(current, lines, index)
            continue

        if line.startswith("@@"):
            hunk, index = _parse_hunk(lines, index)
            if hunk is not None:
                current.hunks.append(hunk)
            continue

        index += 1

    if not changes:
        raise DiffParseError("No file changes found in diff.")

    for change in changes:
        change.change_type = _infer_change_type(change)

    return changes


def _start_file_change(line: str) -> DiffFileChange:
    parts = line.split()
    old_path = _clean_path(parts[2]) if len(parts) >= 4 else None
    new_path = _clean_path(parts[3]) if len(parts) >= 4 else None
    return DiffFileChange(
        old_path=old_path,
        new_path=new_path,
        change_type="modified",
        hunks=[],
    )


def _start_plain_file_change(
    lines: list[str], index: int
) -> tuple[DiffFileChange | None, int]:
    if index + 1 >= len(lines) or not lines[index + 1].startswith("+++ "):
        LOGGER.warning("Skipping malformed file header: %s", lines[index])
        return None, index + 1

    old_path = _parse_file_header_path(lines[index])
    new_path = _parse_file_header_path(lines[index + 1])
    return (
        DiffFileChange(
            old_path=old_path,
            new_path=new_path,
            change_type="modified",
            hunks=[],
        ),
        index + 2,
    )


def _apply_file_headers(
    change: DiffFileChange, lines: list[str], index: int
) -> int:
    if index + 1 >= len(lines) or not lines[index + 1].startswith("+++ "):
        LOGGER.warning("Skipping malformed file header: %s", lines[index])
        return index + 1

    change.old_path = _parse_file_header_path(lines[index])
    change.new_path = _parse_file_header_path(lines[index + 1])
    return index + 2


def _parse_file_header_path(line: str) -> str | None:
    return _clean_path(line[4:].split("\t", 1)[0])


def _parse_hunk(
    lines: list[str], start_index: int
) -> tuple[DiffHunk | None, int]:
    header = lines[start_index]
    match = HUNK_HEADER_RE.match(header)
    if match is None:
        LOGGER.warning("Skipping malformed hunk header: %s", header)
        return None, _find_next_boundary(lines, start_index + 1)

    old_start = int(match.group("old_start"))
    old_count = int(match.group("old_count") or "1")
    new_start = int(match.group("new_start"))
    new_count = int(match.group("new_count") or "1")
    section_header = match.group("section") or ""

    old_lineno = old_start
    new_lineno = new_start
    old_seen = 0
    new_seen = 0
    hunk_lines: list[DiffLine] = []
    index = start_index + 1

    while index < len(lines) and (old_seen < old_count or new_seen < new_count):
        line = lines[index]

        if line.startswith("diff --git ") or line.startswith("@@"):
            LOGGER.warning("Skipping malformed hunk with truncated body: %s", header)
            return None, index

        if line.startswith("\\"):
            index += 1
            continue

        if not line:
            if old_seen < old_count and new_seen < new_count:
                prefix = " "
                content = ""
            else:
                LOGGER.warning("Skipping malformed hunk line in %s", header)
                return None, _find_next_boundary(lines, index + 1)
        else:
            prefix = line[0]
            content = line[1:]

        if prefix == " ":
            hunk_lines.append(
                DiffLine(
                    line_type="context",
                    old_lineno=old_lineno,
                    new_lineno=new_lineno,
                    content=content,
                )
            )
            old_lineno += 1
            new_lineno += 1
            old_seen += 1
            new_seen += 1
        elif prefix == "+":
            hunk_lines.append(
                DiffLine(
                    line_type="added",
                    old_lineno=None,
                    new_lineno=new_lineno,
                    content=content,
                )
            )
            new_lineno += 1
            new_seen += 1
        elif prefix == "-":
            hunk_lines.append(
                DiffLine(
                    line_type="removed",
                    old_lineno=old_lineno,
                    new_lineno=None,
                    content=content,
                )
            )
            old_lineno += 1
            old_seen += 1
        else:
            LOGGER.warning("Skipping malformed hunk line in %s", header)
            return None, _find_next_boundary(lines, index + 1)

        index += 1

    if old_seen != old_count or new_seen != new_count:
        LOGGER.warning("Skipping malformed hunk with line count mismatch: %s", header)
        return None, _find_next_boundary(lines, index)

    while index < len(lines) and lines[index].startswith("\\"):
        index += 1

    return (
        DiffHunk(
            old_start=old_start,
            old_count=old_count,
            new_start=new_start,
            new_count=new_count,
            section_header=section_header,
            lines=hunk_lines,
        ),
        index,
    )


def _find_next_boundary(lines: list[str], index: int) -> int:
    while index < len(lines):
        if lines[index].startswith("diff --git ") or lines[index].startswith("@@"):
            return index
        index += 1
    return index


def _apply_binary_paths(change: DiffFileChange, line: str) -> None:
    if "/dev/null and " in line:
        change.old_path = None
        change.new_path = _clean_path(line.rsplit(" and ", 1)[1].removesuffix(" differ"))
    elif " and /dev/null" in line:
        change.old_path = _clean_path(
            line.removeprefix("Binary files ").split(" and ", 1)[0]
        )
        change.new_path = None


def _infer_change_type(change: DiffFileChange) -> str:
    if change.change_type == "renamed":
        return "renamed"
    if change.old_path is None and change.new_path is not None:
        return "added"
    if change.old_path is not None and change.new_path is None:
        return "deleted"
    return "modified"


def _clean_path(raw_path: str | None) -> str | None:
    if raw_path is None:
        return None

    path = raw_path.strip().strip('"')
    if path == "/dev/null":
        return None
    if path.startswith("a/") or path.startswith("b/"):
        return path[2:]
    return path
