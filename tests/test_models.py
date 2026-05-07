from __future__ import annotations

from code_review_agent.models import (
    AgentRun,
    ChangedEntity,
    ContextRequest,
    CritiqueResult,
    DiffFileChange,
    DiffHunk,
    DiffLine,
    EvidencePackage,
    FileClassification,
    MoveSuggestion,
    PriorFeedback,
    PythonModuleSummary,
    RepoMap,
    ReviewEvidence,
    ReviewIssue,
    ReviewReport,
    ReviewerContext,
    ReviewShard,
    RiskSignal,
    ShardReviewResult,
    StyleBaseline,
    SymbolSummary,
    UncertainFeedbackItem,
)


def test_file_classification_and_move_suggestion() -> None:
    classification = FileClassification(
        path="download_data.py",
        category="data_script",
        mainline_relevance="low",
        confidence=0.86,
        reason="Data helper script.",
    )
    suggestion = MoveSuggestion(
        source_path="download_data.py",
        suggested_path="scripts/data/download_data.py",
        category="data_script",
        reason="Move data helpers under scripts/data.",
        confidence=0.86,
    )

    assert classification.to_dict()["category"] == "data_script"
    assert suggestion.to_dict()["suggested_path"] == "scripts/data/download_data.py"


def test_review_issue_has_confidence_and_evidence_ids() -> None:
    issue = ReviewIssue(
        file="src/app.py",
        line=12,
        severity="medium",
        category="test_gap",
        message="Business logic changed but no related test was updated.",
        suggestion="Add or update tests covering this change.",
        confidence=0.82,
        evidence_ids=["diff:src/app.py:12", "test_discovery:tests/test_app.py"],
    )

    data = issue.to_dict()
    assert data["line"] == 12
    assert data["confidence"] == 0.82
    assert "diff:src/app.py:12" in data["evidence_ids"]


def test_review_issue_defaults_to_empty_evidence() -> None:
    issue = ReviewIssue(
        file="src/app.py",
        line=None,
        severity="info",
        category="maintainability",
        message="No evidence required for this info note.",
        suggestion="No action required.",
    )

    data = issue.to_dict()
    assert data["confidence"] == 0.0
    assert data["evidence_ids"] == []


def test_review_evidence_to_dict() -> None:
    evidence = ReviewEvidence(
        id="diff:src/shop/service.py:35",
        kind="diff",
        source="src/shop/service.py:35",
        message="Validation branch changed in create_order.",
    )

    data = evidence.to_dict()
    assert data["id"] == "diff:src/shop/service.py:35"
    assert data["kind"] == "diff"


def test_context_models_serialize_nested_dataclasses() -> None:
    method = SymbolSummary(
        path="src/shop/service.py",
        symbol_type="method",
        name="create",
        qualified_name="OrderService.create",
        line_start=10,
        line_end=22,
    )
    module = PythonModuleSummary(
        path="src/shop/service.py",
        module_docstring="Order service helpers.",
        imports=["dataclasses.dataclass"],
        classes=[method],
        functions=[],
        methods=[method],
    )
    baseline = StyleBaseline(
        docstring_coverage_ratio=0.0,
        dominant_import_style="mixed",
        test_naming_pattern=None,
        dominant_exception_handling="mixed",
        total_public_functions=0,
    )
    repo_map = RepoMap(
        root=".",
        files=["src/shop/service.py"],
        python_modules=[module],
        imports={"src/shop/service.py": ["dataclasses.dataclass"]},
        imported_by={},
        related_tests={"src/shop/service.py": ["tests/test_service.py"]},
        style_baseline=baseline,
    )

    data = repo_map.to_dict()
    assert data["python_modules"][0]["classes"][0]["qualified_name"] == (
        "OrderService.create"
    )
    assert data["python_modules"][0]["methods"][0]["symbol_type"] == "method"
    assert data["style_baseline"]["total_public_functions"] == 0
    assert data["related_tests"]["src/shop/service.py"] == ["tests/test_service.py"]


def test_diff_models_serialize_line_numbers() -> None:
    hunk = DiffHunk(
        old_start=1,
        old_count=1,
        new_start=1,
        new_count=2,
        section_header="def normalize_name(name):",
        lines=[
            DiffLine(
                line_type="context",
                old_lineno=1,
                new_lineno=1,
                content="def normalize_name(name):",
            ),
            DiffLine(
                line_type="added",
                old_lineno=None,
                new_lineno=2,
                content="    return name.strip().lower()",
            ),
        ],
    )
    change = DiffFileChange(
        old_path="src/app.py",
        new_path="src/app.py",
        change_type="modified",
        hunks=[hunk],
    )

    data = change.to_dict()
    assert data["change_type"] == "modified"
    assert data["hunks"][0]["lines"][1]["old_lineno"] is None
    assert data["hunks"][0]["lines"][1]["new_lineno"] == 2


def test_review_pipeline_models_serialize_references() -> None:
    entity = ChangedEntity(
        path="src/shop/service.py",
        entity_type="function",
        name="create_order",
        qualified_name="create_order",
        line_start=30,
        line_end=45,
        hunk_ids=["src/shop/service.py:30"],
    )
    risk = RiskSignal(
        tag="test_gap",
        confidence=0.82,
        reason="Related tests exist but no test file changed.",
        evidence_ids=["diff:src/shop/service.py:35"],
    )
    evidence = ReviewEvidence(
        id="diff:src/shop/service.py:35",
        kind="diff",
        source="src/shop/service.py:35",
        message="Changed validation branch.",
    )
    package = EvidencePackage(
        repo_root=".",
        changed_entities=[entity],
        risk_signals=[risk],
        evidence_index={evidence.id: evidence},
        metadata={"redacted": ["pr_title", "commit_message"]},
    )
    agent_run = AgentRun(
        agent_name="rules",
        model=None,
        prompt_hash=None,
        input_evidence_ids=[evidence.id],
        output_issue_ids=["issue-1"],
        fallback_used=True,
    )

    package_data = package.to_dict()
    agent_data = agent_run.to_dict()
    assert package_data["changed_entities"][0]["hunk_ids"] == [
        "src/shop/service.py:30"
    ]
    assert package_data["risk_signals"][0]["tag"] == "test_gap"
    assert package_data["evidence_index"][evidence.id]["kind"] == "diff"
    assert agent_data["fallback_used"] is True


def test_loop_feedback_models_serialize() -> None:
    feedback_item = UncertainFeedbackItem(
        issue_id="test_gap:src/app.py:12",
        category="test_gap",
        critic_reason="low confidence",
        original_confidence=0.55,
        evidence_ids=["diff:src/app.py:12"],
    )
    prior_feedback = PriorFeedback(iteration=0, uncertain_items=[feedback_item])
    critique = CritiqueResult(uncertain=[feedback_item])

    assert prior_feedback.to_dict()["uncertain_items"][0]["critic_reason"] == (
        "low confidence"
    )
    assert critique.to_dict()["uncertain"][0]["issue_id"] == (
        "test_gap:src/app.py:12"
    )


def test_agent_run_loop_and_tracing_defaults() -> None:
    run = AgentRun(agent_name="fake", model="fake-llm", prompt_hash="abc")

    data = run.to_dict()
    assert data["iteration"] == 0
    assert data["feedback_hash"] == ""
    assert data["retry_count"] == 0
    assert data["retry_log"] == []
    assert data["latency_ms"] == 0
    assert data["token_count_in"] == 0
    assert data["token_count_out"] == 0
    assert data["status"] == "ok"


def test_reviewer_context_models_serialize() -> None:
    request = ContextRequest(
        request_type="risk_evidence",
        path="src/app.py",
        risk_tag="test_gap",
        reason="Need the risk summary.",
    )
    context = ReviewerContext(
        schema="live_review_input_v1",
        selection_strategy="risk_first_v1",
        repo_root="/repo",
        shard_id="shard-001",
        shard_index=0,
        shard_count=2,
        evidence_index={
            "diff:src/app.py:2": {
                "id": "diff:src/app.py:2",
                "kind": "diff",
                "source": "src/app.py:2",
                "message": "Added line.",
            }
        },
    )
    shard = ReviewShard(
        shard_id="shard-001",
        shard_index=0,
        shard_count=2,
        paths=["src/app.py"],
        selected_evidence_ids=["diff:src/app.py:2"],
    )
    result = ShardReviewResult(
        shard_id="shard-001",
        context_requests=[request],
        status="ok",
    )

    assert context.to_dict()["shard_count"] == 2
    assert shard.to_dict()["paths"] == ["src/app.py"]
    assert result.to_dict()["context_requests"][0]["request_type"] == "risk_evidence"


def test_new_models_use_slots() -> None:
    models = [
        SymbolSummary,
        PythonModuleSummary,
        RepoMap,
        StyleBaseline,
        DiffLine,
        DiffHunk,
        DiffFileChange,
        ChangedEntity,
        RiskSignal,
        EvidencePackage,
        ContextRequest,
        ReviewerContext,
        ReviewShard,
        ShardReviewResult,
        UncertainFeedbackItem,
        PriorFeedback,
        AgentRun,
        CritiqueResult,
    ]

    for model in models:
        assert hasattr(model, "__slots__")


def test_review_report_aggregates_nested_models() -> None:
    issue = ReviewIssue(
        file="src/app.py",
        line=None,
        severity="info",
        category="maintainability",
        message="Info note.",
        suggestion="No action required.",
    )
    classification = FileClassification(
        path="todo.md",
        category="todo",
        mainline_relevance="low",
        confidence=0.9,
        reason="Planning note.",
    )
    suggestion = MoveSuggestion(
        source_path="todo.md",
        suggested_path="docs/planning/todo.md",
        category="todo",
        reason="Planning docs belong under docs/planning.",
        confidence=0.9,
    )
    report = ReviewReport(
        summary={"issue_count": 1},
        issues=[issue],
        file_classifications=[classification],
        move_suggestions=[suggestion],
        project_artifacts_draft="# Project Artifacts",
    )

    data = report.to_dict()
    assert data["summary"]["issue_count"] == 1
    assert data["issues"][0]["file"] == "src/app.py"
    assert data["file_classifications"][0]["category"] == "todo"
    assert data["move_suggestions"][0]["suggested_path"] == "docs/planning/todo.md"
    assert data["project_artifacts_draft"] == "# Project Artifacts"
