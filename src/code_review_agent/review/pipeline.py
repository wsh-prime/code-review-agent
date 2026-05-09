"""Rules-only review pipeline for local unified diffs."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Any

from code_review_agent.context.repo_map import build_repo_map
from code_review_agent.models import (
    AgentRun,
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
    FakeLLMCriticAgent,
    FakeLLMReviewAgent,
    OpenAICompatibleReviewAgent,
    _AgentFatalError,
    _AgentTransientError,
    export_agent_prompts,
)
from code_review_agent.review.changed_entity import extract_changed_entities
from code_review_agent.review.context_budget import (
    DEFAULT_CONTEXT_BUDGET_TOKENS,
    DEFAULT_MAX_EVIDENCE_PER_FILE,
    DEFAULT_MAX_FILES_PER_AGENT_CALL,
    aggregate_context_budget,
    build_reviewer_contexts,
    context_budget_disabled_summary,
)
from code_review_agent.review.diff_parser import parse_unified_diff
from code_review_agent.review.evidence import (
    build_evidence_package,
    find_missing_evidence_ids,
)
from code_review_agent.review.filter import filter_issues
from code_review_agent.review.loop import (
    LOOP_CHECKPOINT_FILENAME,
    IterativeHarnessRunner,
    _all_agent_runs,
    _exclude_final,
    _iteration_record_from_dict,
    _merge_duplicates,
    LoopResult,
)
from code_review_agent.review.risk import (
    API_CHANGE,
    BEHAVIOR_CHANGE,
    CONFIG_CHANGE,
    ERROR_HANDLING_CHANGE,
    SECURITY_SENSITIVE,
    classify_risks,
    risk_evidence_id,
)
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
    max_iter: int = 2,
    resume: bool = False,
    context_budget: int = DEFAULT_CONTEXT_BUDGET_TOKENS,
    max_files_per_agent_call: int = DEFAULT_MAX_FILES_PER_AGENT_CALL,
    max_evidence_per_file: int = DEFAULT_MAX_EVIDENCE_PER_FILE,
    max_context_refill_rounds: int = 1,
    max_context_requests: int = 8,
) -> dict[str, Any]:
    """Run the MVP review pipeline and write JSON/Markdown reports."""

    if mode not in {"rules", "hybrid-fake", "hybrid-live"}:
        raise ValueError("Supported review modes are: rules, hybrid-fake, hybrid-live.")

    repo = Path(repo_path)
    diff_file = Path(diff_path)
    out = Path(out_path)
    effective_mode = mode
    if mode in {"hybrid-fake", "hybrid-live"} and not resume:
        _clear_stale_checkpoints(out)

    diff_text = diff_file.read_text(encoding="utf-8", errors="replace")
    diff_hash = _stable_hash_text(diff_text)
    changes = parse_unified_diff(diff_text)
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
    agent_candidate_scope: list[ReviewIssue] = []
    loop_result: LoopResult | None = None
    changed_paths = _changed_paths(changes)
    package_hash = _stable_hash_value(package.to_dict())
    context_budget_report = context_budget_disabled_summary()
    if mode == "hybrid-fake":
        loop_result = IterativeHarnessRunner(
            reviewer=FakeLLMReviewAgent(),
            critic=FakeLLMCriticAgent(),
            max_iter=max_iter,
            out_dir=out,
            mode=mode,
            diff_hash=diff_hash,
        ).run(package, changed_paths, resume=resume)
        agent_findings = loop_result.final_issues
        agent_needs_human_review = loop_result.needs_human_review
        agent_runs = loop_result.agent_runs
        agent_candidate_scope = _loop_candidate_scope(loop_result)
    elif mode == "hybrid-live":
        reviewer = None
        preview_contexts = build_reviewer_contexts(
            package,
            max_input_tokens=context_budget,
            max_files=max_files_per_agent_call,
            max_evidence_per_file=max_evidence_per_file,
        )
        context_budget_report = aggregate_context_budget(preview_contexts)
        try:
            reviewer = OpenAICompatibleReviewAgent.from_env()
            _configure_live_reviewer(
                reviewer,
                context_budget=context_budget,
                max_files_per_agent_call=max_files_per_agent_call,
                max_evidence_per_file=max_evidence_per_file,
                max_context_refill_rounds=max_context_refill_rounds,
                max_context_requests=max_context_requests,
                out_dir=out,
                package_hash=package_hash,
                diff_hash=diff_hash,
                resume=resume,
            )
            loop_result = IterativeHarnessRunner(
                reviewer=reviewer,
                critic=FakeLLMCriticAgent(),
                max_iter=max_iter,
                out_dir=out,
                mode=mode,
                diff_hash=diff_hash,
            ).run(package, changed_paths, resume=resume)
            agent_findings = loop_result.final_issues
            agent_needs_human_review = loop_result.needs_human_review
            agent_runs = loop_result.agent_runs
            agent_candidate_scope = _loop_candidate_scope(loop_result)
            live_budget = getattr(reviewer, "last_context_budget", None)
            if isinstance(live_budget, dict) and live_budget:
                context_budget_report = live_budget
        except (ValueError, _AgentFatalError, _AgentTransientError) as exc:
            effective_mode = "hybrid-live/fallback-rules"
            fallback_runs = _fallback_agent_runs(exc, reviewer)
            loop_result = _partial_loop_result_from_checkpoint(
                out,
                mode=mode,
                package_hash=package_hash,
                diff_hash=diff_hash,
                fallback_reason=str(exc),
                fallback_runs=fallback_runs,
                resume_used=False,
                resume_ignored_reason=None,
            ) or LoopResult(
                final_issues=[],
                agent_runs=fallback_runs,
                iterations_completed=0,
                converged=False,
                fallback_used=True,
                fallback_reason=str(exc),
            )
            agent_runs = loop_result.agent_runs
            agent_findings = loop_result.final_issues
            agent_needs_human_review = loop_result.needs_human_review
            agent_candidate_scope = _loop_candidate_scope(loop_result)
            live_budget = getattr(reviewer, "last_context_budget", None)
            if isinstance(live_budget, dict) and live_budget:
                context_budget_report = live_budget
            agent_needs_human_review.extend(_fallback_risk_review_issues(
                package,
                existing_issues=[
                    *rules_result.findings,
                    *rules_result.needs_human_review,
                    *agent_findings,
                    *agent_needs_human_review,
                ],
            ))

    candidate_findings = [*rules_result.findings, *agent_findings]
    candidate_needs_human_review = [
        *rules_result.needs_human_review,
        *agent_needs_human_review,
    ]
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
            mode=effective_mode,
            pair_strategy=CROSS_STRATEGY,
            context_budget_tokens=context_budget,
            max_files_per_agent_call=max_files_per_agent_call,
            max_evidence_per_file=max_evidence_per_file,
        )
        if export_prompts
        else {}
    )

    report = _build_report_dict(
        mode=effective_mode,
        package=package,
        findings=findings,
        needs_human_review=needs_human_review,
        candidate_issues=[
            *candidate_findings,
            *candidate_needs_human_review,
            *agent_candidate_scope,
        ],
        discarded=[
            *filter_result.to_dict()["discarded"],
            *_loop_discarded(loop_result),
        ],
        agent_runs=agent_runs,
        prompt_exports=prompt_exports,
        loop_result=loop_result,
        max_iter=max_iter,
        context_budget=context_budget_report,
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
    loop_result: LoopResult | None = None,
    max_iter: int = 2,
    context_budget: dict[str, Any] | None = None,
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
    loop_data = _loop_report(loop_result, max_iter=max_iter)
    tracing_data = _tracing_report(agent_run_items)
    context_budget_data = context_budget or context_budget_disabled_summary()
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
            "loop_enabled": loop_result is not None,
            "loop_iterations_completed": (
                loop_result.iterations_completed if loop_result is not None else 0
            ),
            "loop_converged": (
                loop_result.converged if loop_result is not None else False
            ),
            "fallback_used": (
                loop_result.fallback_used if loop_result is not None else False
            ),
            "fallback_reason": (
                loop_result.fallback_reason if loop_result is not None else None
            ),
            "resume_used": (
                loop_result.resume_used if loop_result is not None else False
            ),
            "resume_ignored_reason": (
                loop_result.resume_ignored_reason
                if loop_result is not None
                else None
            ),
            "total_latency_ms": tracing_data["total_latency_ms"],
            "total_token_count_in": tracing_data["total_token_count_in"],
            "total_token_count_out": tracing_data["total_token_count_out"],
            "context_budget_enabled": bool(context_budget_data.get("enabled", False)),
            "context_truncated": bool(
                context_budget_data.get("context_truncated", False)
            ),
            "selected_evidence_count": int(
                context_budget_data.get("selected_evidence_count", 0)
            ),
            "omitted_evidence_count": int(
                context_budget_data.get("omitted_evidence_count", 0)
            ),
            "review_shard_count": int(context_budget_data.get("shard_count", 0)),
            "context_refill_count": int(context_budget_data.get("refill_count", 0)),
            "context_request_count": int(
                context_budget_data.get("context_request_count", 0)
            ),
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
        "context_budget": context_budget_data,
        "loop": loop_data,
        "tracing": tracing_data,
    }



def _changed_paths(changes) -> set[str]:
    paths: set[str] = set()
    for change in changes:
        if change.old_path is not None:
            paths.add(change.old_path)
        if change.new_path is not None:
            paths.add(change.new_path)
    return paths


def _fallback_risk_review_issues(
    package,
    *,
    existing_issues: list[ReviewIssue],
) -> list[ReviewIssue]:
    """Route important non-rule risks to humans when live review cannot run."""

    surfaced = {
        (issue.category, issue.file)
        for issue in existing_issues
    }
    review_tags = {
        API_CHANGE,
        BEHAVIOR_CHANGE,
        CONFIG_CHANGE,
        ERROR_HANDLING_CHANGE,
        SECURITY_SENSITIVE,
    }
    issues: list[ReviewIssue] = []
    for signal in package.risk_signals:
        if signal.tag not in review_tags:
            continue
        path, line = _risk_location(signal)
        if (signal.tag, path) in surfaced:
            continue
        evidence_ids = _risk_issue_evidence_ids(signal, package)
        if not evidence_ids:
            continue
        issues.append(
            ReviewIssue(
                file=path,
                line=line,
                severity="medium",
                category=signal.tag,
                message=(
                    "Live reviewer was unavailable; this deterministic risk "
                    "needs human review."
                ),
                suggestion=(
                    "Inspect the linked evidence and decide whether the "
                    "change requires follow-up."
                ),
                confidence=min(max(signal.confidence, 0.55), 0.74),
                evidence_ids=evidence_ids,
            )
        )
    return issues


def _risk_issue_evidence_ids(signal, package) -> list[str]:
    evidence_ids = list(signal.evidence_ids[:12])
    signal_id = risk_evidence_id(signal)
    if signal_id in package.evidence_index:
        evidence_ids.insert(0, signal_id)
    return sorted(dict.fromkeys(evidence_ids))


def _risk_location(signal) -> tuple[str, int | None]:
    for evidence_id in signal.evidence_ids:
        if not evidence_id.startswith(("diff:", "diff_hunk:", "entity:", "hygiene:")):
            continue
        parts = evidence_id.split(":")
        if len(parts) < 2:
            continue
        line = (
            int(parts[-1])
            if evidence_id.startswith(("diff:", "diff_hunk:")) and parts[-1].isdigit()
            else None
        )
        path = (
            ":".join(parts[1:-1])
            if evidence_id.startswith(("diff:", "diff_hunk:"))
            else parts[1]
        )
        return path, line
    return "patch", None


def _loop_candidate_scope(loop_result: LoopResult | None) -> list[ReviewIssue]:
    if loop_result is None:
        return []
    return [item.issue for item in loop_result.discarded]


def _loop_discarded(loop_result: LoopResult | None) -> list[dict[str, Any]]:
    if loop_result is None:
        return []
    return [item.to_dict() for item in loop_result.discarded]


def _loop_report(loop_result: LoopResult | None, *, max_iter: int) -> dict[str, Any]:
    if loop_result is None:
        return {
            "enabled": False,
            "max_iter": max_iter,
            "iterations_completed": 0,
            "converged": False,
            "fallback_used": False,
            "fallback_reason": None,
            "checkpoint_path": None,
            "resume_used": False,
            "resume_ignored_reason": None,
            "iterations": [],
        }
    return {
        "enabled": True,
        "max_iter": max_iter,
        "iterations_completed": loop_result.iterations_completed,
        "converged": loop_result.converged,
        "fallback_used": loop_result.fallback_used,
        "fallback_reason": loop_result.fallback_reason,
        "checkpoint_path": loop_result.checkpoint_path,
        "resume_used": loop_result.resume_used,
        "resume_ignored_reason": loop_result.resume_ignored_reason,
        "iterations": [record.to_dict() for record in loop_result.iterations],
    }


def _configure_live_reviewer(
    reviewer: object,
    *,
    context_budget: int,
    max_files_per_agent_call: int,
    max_evidence_per_file: int,
    max_context_refill_rounds: int,
    max_context_requests: int,
    out_dir: Path,
    package_hash: str,
    diff_hash: str,
    resume: bool,
) -> None:
    for name, value in {
        "context_budget_tokens": context_budget,
        "max_files_per_agent_call": max_files_per_agent_call,
        "max_evidence_per_file": max_evidence_per_file,
        "max_context_refill_rounds": max_context_refill_rounds,
        "max_context_requests": max_context_requests,
        "context_checkpoint_path": str(out_dir / "live_context_checkpoint.json"),
        "context_checkpoint_package_hash": package_hash,
        "context_checkpoint_diff_hash": diff_hash,
        "context_checkpoint_resume": resume,
    }.items():
        if hasattr(reviewer, name):
            setattr(reviewer, name, value)


def _clear_stale_checkpoints(out_dir: Path) -> None:
    for name in (LOOP_CHECKPOINT_FILENAME, "live_context_checkpoint.json"):
        path = out_dir / name
        if path.is_file() or path.is_symlink():
            path.unlink()


def _partial_loop_result_from_checkpoint(
    out_dir: Path,
    *,
    mode: str,
    package_hash: str,
    diff_hash: str,
    fallback_reason: str,
    fallback_runs: list[AgentRun],
    resume_used: bool,
    resume_ignored_reason: str | None,
) -> LoopResult | None:
    path = out_dir / LOOP_CHECKPOINT_FILENAME
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if data.get("mode") != mode:
        return None
    if data.get("package_hash") != package_hash or data.get("diff_hash") != diff_hash:
        return None
    records = [
        _iteration_record_from_dict(item)
        for item in data.get("iterations", [])
        if isinstance(item, dict)
    ]
    if not records:
        return None
    final_issues = list(records[-1].keep)
    needs_human_review = [
        issue for record in records for issue in record.needs_human_review
    ]
    discarded = [item for record in records for item in record.discarded]
    return LoopResult(
        final_issues=final_issues,
        needs_human_review=_exclude_final(
            _merge_duplicates(needs_human_review),
            final_issues,
        ),
        discarded=discarded,
        agent_runs=[*_all_agent_runs(records), *fallback_runs],
        iterations=records,
        iterations_completed=len(records),
        converged=False,
        fallback_used=True,
        fallback_reason=fallback_reason,
        checkpoint_path=str(path),
        resume_used=resume_used,
        resume_ignored_reason=resume_ignored_reason,
    )


def _tracing_report(agent_runs: list) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    for run in agent_runs:
        status = run.status or "unknown"
        status_counts[status] = status_counts.get(status, 0) + 1
    return {
        "total_latency_ms": sum(run.latency_ms for run in agent_runs),
        "total_token_count_in": sum(run.token_count_in for run in agent_runs),
        "total_token_count_out": sum(run.token_count_out for run in agent_runs),
        "total_retry_count": sum(run.retry_count for run in agent_runs),
        "run_count": len(agent_runs),
        "status_counts": status_counts,
    }


def _fallback_agent_runs(exc: Exception, reviewer: object | None) -> list[AgentRun]:
    live_runs = getattr(reviewer, "last_agent_runs", None)
    if isinstance(live_runs, list) and live_runs:
        runs = [
            run
            for run in live_runs
            if isinstance(run, AgentRun)
        ]
        if runs:
            runs[-1] = _fallback_agent_run_from_live(exc, runs[-1])
            return runs
    return [_fallback_agent_run_from_reviewer(exc, reviewer)]


def _fallback_agent_run_from_live(exc: Exception, live_run: AgentRun) -> AgentRun:
    return AgentRun(
        agent_name=live_run.agent_name,
        model=live_run.model,
        prompt_hash=live_run.prompt_hash,
        input_evidence_ids=list(live_run.input_evidence_ids),
        output_issue_ids=list(live_run.output_issue_ids),
        fallback_used=True,
        iteration=live_run.iteration,
        feedback_hash=live_run.feedback_hash,
        retry_count=live_run.retry_count,
        retry_log=list(live_run.retry_log),
        latency_ms=live_run.latency_ms,
        token_count_in=live_run.token_count_in,
        token_count_out=live_run.token_count_out,
        trace_id=live_run.trace_id,
        span_id=live_run.span_id,
        parent_span_id=live_run.parent_span_id,
        status="fallback",
        error_type=exc.__class__.__name__,
        shard_id=live_run.shard_id,
        shard_index=live_run.shard_index,
        shard_count=live_run.shard_count,
        context_request_count=live_run.context_request_count,
        context_refill_used=live_run.context_refill_used,
    )


def _fallback_agent_run_from_reviewer(
    exc: Exception,
    reviewer: object | None,
) -> AgentRun:
    live_run = getattr(reviewer, "last_agent_run", None)
    if isinstance(live_run, AgentRun):
        return _fallback_agent_run_from_live(exc, live_run)
    return AgentRun(
        agent_name="openai_compatible_reviewer",
        model=getattr(reviewer, "model", None),
        prompt_hash=None,
        fallback_used=True,
        status="fallback",
        error_type=exc.__class__.__name__,
    )


def _stable_hash_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _stable_hash_value(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False)
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


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
