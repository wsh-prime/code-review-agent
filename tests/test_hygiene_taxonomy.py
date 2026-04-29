"""Tests for hygiene.taxonomy module."""

from __future__ import annotations

from code_review_agent.hygiene.taxonomy import (
    ALL_TYPES,
    DESCRIPTIONS,
    MOVE_TYPES,
    REVIEW_TYPES,
    SUGGESTED_ACTIONS,
    TARGET_DIRS,
    UNCERTAIN,
)


def test_all_types_are_seven() -> None:
    assert len(ALL_TYPES) == 7


def test_every_type_has_a_description() -> None:
    assert ALL_TYPES == set(DESCRIPTIONS.keys())


def test_every_type_has_a_suggested_action() -> None:
    assert ALL_TYPES == set(SUGGESTED_ACTIONS.keys())


def test_move_and_review_types_partition_all_types() -> None:
    # MOVE_TYPES ∪ REVIEW_TYPES should equal ALL_TYPES, no overlap.
    assert MOVE_TYPES | REVIEW_TYPES == ALL_TYPES
    assert MOVE_TYPES & REVIEW_TYPES == frozenset()


def test_move_types_have_target_dirs() -> None:
    for t in MOVE_TYPES:
        assert t in TARGET_DIRS, f"{t!r} has no target directory"


def test_review_types_have_no_target_dir() -> None:
    for t in REVIEW_TYPES:
        assert t not in TARGET_DIRS, f"{t!r} should not have a target directory"


def test_move_types_suggest_move_or_document() -> None:
    valid_actions = {"move", "document"}
    for t in MOVE_TYPES:
        assert SUGGESTED_ACTIONS[t] in valid_actions


def test_review_types_suggest_needs_human_review() -> None:
    for t in REVIEW_TYPES:
        assert SUGGESTED_ACTIONS[t] == "needs_human_review"


def test_uncertain_is_in_review_types() -> None:
    assert UNCERTAIN in REVIEW_TYPES


def test_descriptions_are_non_empty_strings() -> None:
    for t, desc in DESCRIPTIONS.items():
        assert isinstance(desc, str) and len(desc) > 20, (
            f"Description for {t!r} is too short or not a string"
        )
