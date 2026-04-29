"""Map parsed diff hunks to changed Python entities."""

from __future__ import annotations

from pathlib import Path

from code_review_agent.models import (
    ChangedEntity,
    DiffFileChange,
    DiffHunk,
    RepoMap,
    SymbolSummary,
)


def extract_changed_entities(
    changes: list[DiffFileChange], repo_map: RepoMap
) -> list[ChangedEntity]:
    """Return changed entities for each hunk, falling back to module level."""

    entities: dict[tuple[str, str, str], ChangedEntity] = {}

    for change in changes:
        path = change.new_path or change.old_path
        if path is None:
            continue

        symbols = _symbols_for_module(path, repo_map)

        if not change.hunks:
            entity = _module_entity(path, [1], _hunk_id(path, 1))
            _merge_entity(entities, entity)
            continue

        for hunk in change.hunks:
            hunk_id = _hunk_id(path, hunk.new_start if change.new_path else hunk.old_start)
            changed_lines = _changed_line_numbers(hunk, prefer_new=change.new_path is not None)

            unmatched_lines: list[int] = []
            for line_number in changed_lines:
                symbol = _innermost_symbol(symbols, line_number)
                if symbol is None:
                    unmatched_lines.append(line_number)
                    continue
                _merge_entity(
                    entities,
                    ChangedEntity(
                        path=path,
                        entity_type=symbol.symbol_type,
                        name=symbol.name,
                        qualified_name=symbol.qualified_name,
                        line_start=symbol.line_start,
                        line_end=symbol.line_end,
                        hunk_ids=[hunk_id],
                    ),
                )

            if unmatched_lines:
                _merge_entity(
                    entities,
                    _module_entity(path, unmatched_lines, hunk_id),
                )

    return sorted(
        entities.values(),
        key=lambda entity: (entity.path, entity.line_start, entity.qualified_name),
    )


def _symbols_for_module(path: str, repo_map: RepoMap) -> list[SymbolSummary]:
    for module in repo_map.python_modules:
        if module.path == path:
            return [*module.classes, *module.functions, *module.methods]
    return []


def _changed_line_numbers(hunk: DiffHunk, *, prefer_new: bool) -> list[int]:
    numbers: list[int] = []
    for line in hunk.lines:
        if line.line_type == "context":
            continue
        number = line.new_lineno if prefer_new else line.old_lineno
        if number is None:
            number = line.old_lineno if prefer_new else line.new_lineno
        if number is not None:
            numbers.append(number)

    return numbers or [hunk.new_start if prefer_new else hunk.old_start]


def _innermost_symbol(
    symbols: list[SymbolSummary], line_number: int
) -> SymbolSummary | None:
    containing = [
        symbol
        for symbol in symbols
        if symbol.line_start <= line_number <= symbol.line_end
    ]
    if not containing:
        return None

    return min(
        containing,
        key=lambda symbol: (
            symbol.line_end - symbol.line_start,
            _symbol_priority(symbol.symbol_type),
        ),
    )


def _symbol_priority(symbol_type: str) -> int:
    priorities = {"method": 0, "function": 1, "class": 2}
    return priorities.get(symbol_type, 3)


def _module_entity(path: str, changed_lines: list[int], hunk_id: str) -> ChangedEntity:
    line_start = min(changed_lines) if changed_lines else 1
    line_end = max(changed_lines) if changed_lines else line_start
    name = Path(path).name
    qualified_name = Path(path).with_suffix("").as_posix().replace("/", ".")
    return ChangedEntity(
        path=path,
        entity_type="module",
        name=name,
        qualified_name=qualified_name,
        line_start=line_start,
        line_end=line_end,
        hunk_ids=[hunk_id],
    )


def _merge_entity(
    entities: dict[tuple[str, str, str], ChangedEntity], entity: ChangedEntity
) -> None:
    key = (entity.path, entity.entity_type, entity.qualified_name)
    existing = entities.get(key)
    if existing is None:
        entities[key] = entity
        return

    for hunk_id in entity.hunk_ids:
        if hunk_id not in existing.hunk_ids:
            existing.hunk_ids.append(hunk_id)


def _hunk_id(path: str, start_line: int) -> str:
    return f"{path}:{start_line}"
