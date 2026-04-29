from __future__ import annotations

from code_review_agent.hygiene.planner import (
    build_move_suggestions,
    build_project_artifacts_draft,
)
from code_review_agent.models import FileClassification


def test_build_move_suggestions_avoids_existing_target(tmp_path) -> None:
    repo = tmp_path / "repo"
    (repo / "docs" / "planning").mkdir(parents=True)
    (repo / "todo.md").write_text("- [ ] root task\n", encoding="utf-8")
    (repo / "docs" / "planning" / "todo.md").write_text("existing\n", encoding="utf-8")
    classification = FileClassification(
        path="todo.md",
        category="todo",
        mainline_relevance="low",
        confidence=0.9,
        reason="Task list belongs under planning docs.",
        signals=["filename starts with todo"],
    )

    suggestions = build_move_suggestions(repo, [classification])

    assert len(suggestions) == 1
    assert suggestions[0].suggested_path == "docs/planning/todo_2.md"
    assert (repo / "todo.md").exists()


def test_project_artifacts_draft_groups_suggestions(tmp_path) -> None:
    classification = FileClassification(
        path="download_data.py",
        category="data_script",
        mainline_relevance="low",
        confidence=0.86,
        reason="Data helper script.",
        signals=["filename contains download"],
    )
    suggestions = build_move_suggestions(tmp_path, [classification])

    draft = build_project_artifacts_draft([classification], suggestions)

    assert "# Project Artifacts" in draft
    assert "## data_script" in draft
    assert "`download_data.py`" in draft
    assert "`scripts/data/download_data.py`" in draft
