"""Rules-only review pipeline for local unified diffs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from code_review_agent.context.repo_map import build_repo_map
from code_review_agent.models import (
    FileClassification,
    PythonModuleSummary,
    RepoMap,
    ReviewIssue,
    StyleBaseline,
    SymbolSummary,
)
from code_review_agent.output.json_report import (
    REVIEW_REPORT_SCHEMA_VERSION,
    normalize_review_report,
    write_review_json,
)
from code_review_agent.output.review_markdown import render_review_markdown
from code_review_agent.review.agents import (
    CROSS_STRATEGY,
    export_agent_prompts,
    run_fake_hybrid_agents,
    run_openai_compatible_review_agent,
)
from code_review_agent.review.changed_entity import extract_changed_entities
from code_review_agent.review.diff_parser import parse_unified_diff
from code_review_agent.review.evidence import (
    build_evidence_package,
    find_missing_evidence_ids,
)
from code_review_agent.review.filter import filter_issues
from code_review_agent.review.risk import classify_risks
from code_review_agent.review.rules import run_rules



def run_review_pipeline(
    repo_path: Path | str,
    diff_path: Path | str,
    out_path: Path | str,
    *,
    repo_map_path: Path | str | None = None,
    hygiene_path: Path | str | None = None,
    mode: str = "rules",
    export_prompts: bool = False,
) -> dict[str, Any]:
    """Run the MVP review pipeline and write JSON/Markdown reports."""

    if mode not in {"rules", "hybrid-fake", "hybrid-live"}:
        raise ValueError("Supported review modes are: rules, hybrid-fake, hybrid-live.")

    repo = Path(repo_path)
    diff_file = Path(diff_path)
    out = Path(out_path)

    changes = parse_unified_diff(diff_file.read_text(encoding="utf-8", errors="replace"))
    repo_map = (
        load_repo_map(repo_map_path)
        if repo_map_path is not None
        else build_repo_map(repo)
    )
    hygiene_classifications = (
        load_hygiene_classifications(hygiene_path)
        if hygiene_path is not None
        else []
    )
    changed_entities = extract_changed_entities(changes, repo_map)
    risk_signals = classify_risks(
        changes,
        repo_map,
        changed_entities,
        hygiene_classifications=hygiene_classifications,
    )
    package = build_evidence_package(
        repo,
        changes,
        changed_entities,
        risk_signals,
        repo_map,
        hygiene_classifications=hygiene_classifications,
    )
    rules_result = run_rules(package)
    agent_runs = []
    agent_findings: list[ReviewIssue] = []
    agent_needs_human_review: list[ReviewIssue] = []
    if mode == "hybrid-fake":
        fake_result = run_fake_hybrid_agents(package, pair_strategy=CROSS_STRATEGY)
        agent_findings = fake_result.findings
        agent_needs_human_review = fake_result.needs_human_review
        agent_runs = fake_result.agent_runs
    elif mode == "hybrid-live":
        live_result = run_openai_compatible_review_agent(package)
        agent_findings = live_result.findings
        agent_needs_human_review = live_result.needs_human_review
        agent_runs = live_result.agent_runs

    candidate_findings = [*rules_result.findings, *agent_findings]
    candidate_needs_human_review = [
        *rules_result.needs_human_review,
        *agent_needs_human_review,
    ]
    changed_paths = _changed_paths(changes)
    filter_result = filter_issues(
        candidate_findings,
        candidate_needs_human_review,
        package,
        changed_paths,
    )
    findings = filter_result.findings
    needs_human_review = filter_result.needs_human_review
    out.mkdir(parents=True, exist_ok=True)
    prompt_exports = (
        export_agent_prompts(
            package,
            out / "prompts",
            mode=mode,
            pair_strategy=CROSS_STRATEGY,
        )
        if export_prompts
        else {}
    )

    report = _build_report_dict(
        mode=mode,
        package=package,
        findings=findings,
        needs_human_review=needs_human_review,
        candidate_issues=[*candidate_findings, *candidate_needs_human_review],
        discarded=filter_result.to_dict()["discarded"],
        agent_runs=agent_runs,
        prompt_exports=prompt_exports,
    )

    json_path = out / "review_report.json"
    markdown_path = out / "review_report.md"
    write_review_json(report, json_path)
    markdown_path.write_text(render_review_report_markdown(report), encoding="utf-8")
    return normalize_review_report(report)


def load_repo_map(path: Path | str) -> RepoMap:
    """Load a RepoMap JSON document written by the map command."""

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    modules = [_python_module_from_dict(item) for item in data.get("python_modules", [])]
    style_data = data.get("style_baseline")
    return RepoMap(
        root=data["root"],
        files=list(data.get("files", [])),
        python_modules=modules,
        imports={key: list(value) for key, value in data.get("imports", {}).items()},
        imported_by={
            key: list(value) for key, value in data.get("imported_by", {}).items()
        },
        related_tests={
            key: list(value) for key, value in data.get("related_tests", {}).items()
        },
        style_baseline=StyleBaseline(**style_data) if style_data is not None else None,
    )


def load_hygiene_classifications(path: Path | str) -> list[FileClassification]:
    """Load file classifications from a hygiene command JSON report."""

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        FileClassification(
            path=item["path"],
            category=item["category"],
            mainline_relevance=item["mainline_relevance"],
            confidence=item["confidence"],
            reason=item["reason"],
            signals=list(item.get("signals", [])),
        )
        for item in data.get("file_classifications", [])
    ]


def render_review_report_markdown(report: dict[str, Any]) -> str:
    """Render review Markdown via the output module."""

    return render_review_markdown(report)


def _build_report_dict(
    *,
    mode: str,
    package,
    findings: list[ReviewIssue],
    needs_human_review: list[ReviewIssue],
    candidate_issues: list[ReviewIssue] | None = None,
    discarded: list[dict[str, Any]] | None = None,
    agent_runs: list | None = None,
    prompt_exports: dict[str, Any] | None = None,
) -> dict[str, Any]:
    evidence_issue_scope = (
        candidate_issues
        if candidate_issues is not None
        else [*findings, *needs_human_review]
    )
    missing_evidence_ids = find_missing_evidence_ids(
        package, issues=evidence_issue_scope
    )
    discarded_items = discarded or []
    agent_run_items = agent_runs or []
    prompt_export_data = prompt_exports or {}
    return {
        "schema_version": REVIEW_REPORT_SCHEMA_VERSION,
        "summary": {
            "mode": mode,
            "changed_file_count": len(package.changed_files),
            "changed_entity_count": len(package.changed_entities),
            "risk_signal_count": len(package.risk_signals),
            "finding_count": len(findings),
            "needs_human_review_count": len(needs_human_review),
            "discarded_count": len(discarded_items),
            "evidence_count": len(package.evidence_index),
            "missing_evidence_id_count": len(missing_evidence_ids),
            "agent_run_count": len(agent_run_items),
            "prompt_exported": bool(prompt_export_data),
            "target_repo_modified": False,
        },
        "findings": [issue.to_dict() for issue in findings],
        "needs_human_review": [
            issue.to_dict() for issue in needs_human_review
        ],
        "discarded": discarded_items,
        "changed_files": [change.to_dict() for change in package.changed_files],
        "changed_entities": [
            entity.to_dict() for entity in package.changed_entities
        ],
        "risk_signals": [signal.to_dict() for signal in package.risk_signals],
        "evidence_index": {
            evidence_id: evidence.to_dict()
            for evidence_id, evidence in package.evidence_index.items()
        },
        "missing_evidence_ids": missing_evidence_ids,
        "agent_runs": [run.to_dict() for run in agent_run_items],
        "prompt_exports": prompt_export_data,
    }



def _changed_paths(changes) -> set[str]:
    paths: set[str] = set()
    for change in changes:
        if change.old_path is not None:
            paths.add(change.old_path)
        if change.new_path is not None:
            paths.add(change.new_path)
    return paths


def _python_module_from_dict(data: dict[str, Any]) -> PythonModuleSummary:
    return PythonModuleSummary(
        path=data["path"],
        module_docstring=data.get("module_docstring"),
        imports=list(data.get("imports", [])),
        classes=[_symbol_from_dict(item) for item in data.get("classes", [])],
        functions=[_symbol_from_dict(item) for item in data.get("functions", [])],
        methods=[_symbol_from_dict(item) for item in data.get("methods", [])],
    )


def _symbol_from_dict(data: dict[str, Any]) -> SymbolSummary:
    return SymbolSummary(
        path=data["path"],
        symbol_type=data["symbol_type"],
        name=data["name"],
        qualified_name=data["qualified_name"],
        line_start=data["line_start"],
        line_end=data["line_end"],
    )
