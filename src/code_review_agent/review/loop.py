"""Iterative review harness for critic-to-reviewer feedback loops."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from code_review_agent.models import (
    AgentRun,
    CritiqueResult,
    EvidencePackage,
    PriorFeedback,
    ReviewIssue,
    UncertainFeedbackItem,
)
from code_review_agent.review.agents import CriticAgent, ReviewAgent, prompt_hash
from code_review_agent.review.verifier import GroundingDiscardedIssue, ground_verify


LOOP_CHECKPOINT_FILENAME = "loop_checkpoint.json"
LOOP_SCHEMA_VERSION = "1.0"


@dataclass(slots=True)
class IterationRecord:
    """Summary for one completed loop iteration."""

    i: int
    candidate_issue_count: int
    verified_count: int
    needs_human_review_count: int
    discarded_count: int
    keep_count: int
    uncertain_count: int
    reject_count: int
    feedback_sent: list[UncertainFeedbackItem] = field(default_factory=list)
    agent_runs: list[AgentRun] = field(default_factory=list)
    issue_set: list[str] = field(default_factory=list)
    keep: list[ReviewIssue] = field(default_factory=list)
    needs_human_review: list[ReviewIssue] = field(default_factory=list)
    discarded: list[GroundingDiscardedIssue] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "i": self.i,
            "candidate_issue_count": self.candidate_issue_count,
            "verified_count": self.verified_count,
            "needs_human_review_count": self.needs_human_review_count,
            "discarded_count": self.discarded_count,
            "keep_count": self.keep_count,
            "uncertain_count": self.uncertain_count,
            "reject_count": self.reject_count,
            "feedback_sent": [item.to_dict() for item in self.feedback_sent],
            "agent_runs": [run.to_dict() for run in self.agent_runs],
            "issue_set": list(self.issue_set),
            "keep": [issue.to_dict() for issue in self.keep],
            "needs_human_review": [
                issue.to_dict() for issue in self.needs_human_review
            ],
            "discarded": [item.to_dict() for item in self.discarded],
        }


@dataclass(slots=True)
class LoopResult:
    """Final result from the iterative harness."""

    final_issues: list[ReviewIssue]
    needs_human_review: list[ReviewIssue] = field(default_factory=list)
    discarded: list[GroundingDiscardedIssue] = field(default_factory=list)
    agent_runs: list[AgentRun] = field(default_factory=list)
    iterations: list[IterationRecord] = field(default_factory=list)
    iterations_completed: int = 0
    converged: bool = False
    fallback_used: bool = False
    fallback_reason: str | None = None
    checkpoint_path: str | None = None
    resume_used: bool = False
    resume_ignored_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "final_issues": [issue.to_dict() for issue in self.final_issues],
            "needs_human_review": [
                issue.to_dict() for issue in self.needs_human_review
            ],
            "discarded": [item.to_dict() for item in self.discarded],
            "agent_runs": [run.to_dict() for run in self.agent_runs],
            "iterations": [record.to_dict() for record in self.iterations],
            "iterations_completed": self.iterations_completed,
            "converged": self.converged,
            "fallback_used": self.fallback_used,
            "fallback_reason": self.fallback_reason,
            "checkpoint_path": self.checkpoint_path,
            "resume_used": self.resume_used,
            "resume_ignored_reason": self.resume_ignored_reason,
        }


@dataclass(slots=True)
class IterativeHarnessRunner:
    """Run reviewer, verifier, and critic for a bounded number of passes."""

    reviewer: ReviewAgent
    critic: CriticAgent
    max_iter: int = 2
    out_dir: Path | None = None
    mode: str = "hybrid-fake"
    package_hash: str = ""
    diff_hash: str = ""
    run_id: str = ""

    def run(
        self,
        package: EvidencePackage,
        changed_paths: set[str],
        *,
        resume: bool = False,
    ) -> LoopResult:
        max_iter = max(1, self.max_iter)
        package_hash = self.package_hash or _stable_hash(package.to_dict())
        diff_hash = self.diff_hash or _stable_hash(
            [change.to_dict() for change in package.changed_files]
        )
        (
            start_i,
            prior_feedback,
            records,
            resume_used,
            resume_ignored_reason,
        ) = self._load_checkpoint(
            resume=resume,
            package_hash=package_hash,
            diff_hash=diff_hash,
        )
        all_needs_human_review: list[ReviewIssue] = [
            issue for record in records for issue in record.needs_human_review
        ]
        all_discarded: list[GroundingDiscardedIssue] = [
            item for record in records for item in record.discarded
        ]
        last_keep: list[ReviewIssue] = list(records[-1].keep) if records else []

        for i in range(start_i, max_iter):
            feedback_hash = _feedback_hash(prior_feedback)
            candidates = self.reviewer.review(
                package, prior_feedback=prior_feedback
            )
            verifier_result = ground_verify(candidates, package, changed_paths)
            all_needs_human_review.extend(verifier_result.needs_human_review)
            all_discarded.extend(verifier_result.discarded)

            critique = self.critic.critique(verifier_result.verified, package)
            last_keep = list(critique.keep)
            unresolved_uncertain = _issues_for_feedback(
                critique.uncertain, verifier_result.verified
            )
            all_needs_human_review.extend(unresolved_uncertain)
            agent_runs = _agent_runs_for_iteration(
                i=i,
                feedback_hash=feedback_hash,
                reviewer=self.reviewer,
                critic=self.critic,
                package=package,
                candidates=candidates,
                verified=verifier_result.verified,
                critique=critique,
            )
            issue_set = _normalized_issue_set(critique)
            record = IterationRecord(
                i=i,
                candidate_issue_count=len(candidates),
                verified_count=len(verifier_result.verified),
                needs_human_review_count=len(verifier_result.needs_human_review),
                discarded_count=len(verifier_result.discarded),
                keep_count=len(critique.keep),
                uncertain_count=len(critique.uncertain),
                reject_count=len(critique.reject),
                feedback_sent=list(critique.uncertain),
                agent_runs=agent_runs,
                issue_set=issue_set,
                keep=list(critique.keep),
                needs_human_review=[
                    *verifier_result.needs_human_review,
                    *unresolved_uncertain,
                ],
                discarded=list(verifier_result.discarded),
            )
            records.append(record)
            converged = _converged(records, critique)
            next_feedback = (
                None
                if converged
                else PriorFeedback(
                    iteration=i,
                    uncertain_items=list(critique.uncertain),
                )
            )
            self._save_checkpoint(
                records,
                next_feedback=next_feedback,
                converged=converged,
                package_hash=package_hash,
                diff_hash=diff_hash,
            )

            if converged:
                return LoopResult(
                    final_issues=critique.keep,
                    needs_human_review=_exclude_final(
                        _merge_duplicates(all_needs_human_review), critique.keep
                    ),
                    discarded=all_discarded,
                    agent_runs=_all_agent_runs(records),
                    iterations=records,
                    iterations_completed=len(records),
                    converged=True,
                    checkpoint_path=self._checkpoint_path_str(),
                    resume_used=resume_used,
                    resume_ignored_reason=resume_ignored_reason,
                )

            prior_feedback = next_feedback

        return LoopResult(
            final_issues=last_keep,
            needs_human_review=_exclude_final(
                _merge_duplicates(all_needs_human_review), last_keep
            ),
            discarded=all_discarded,
            agent_runs=_all_agent_runs(records),
            iterations=records,
            iterations_completed=len(records),
            converged=False,
            checkpoint_path=self._checkpoint_path_str(),
            resume_used=resume_used,
            resume_ignored_reason=resume_ignored_reason,
        )

    def _load_checkpoint(
        self,
        *,
        resume: bool,
        package_hash: str,
        diff_hash: str,
    ) -> tuple[
        int,
        PriorFeedback | None,
        list[IterationRecord],
        bool,
        str | None,
    ]:
        if not resume:
            return 0, None, [], False, None
        if self.out_dir is None:
            return 0, None, [], False, "checkpoint_disabled"
        path = self.out_dir / LOOP_CHECKPOINT_FILENAME
        if not path.exists():
            return 0, None, [], False, "checkpoint_not_found"

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return 0, None, [], False, "checkpoint_invalid_json"

        if data.get("schema_version") != LOOP_SCHEMA_VERSION:
            return 0, None, [], False, "schema_version_mismatch"
        if data.get("mode") != self.mode:
            return 0, None, [], False, "mode_mismatch"
        if data.get("package_hash") != package_hash:
            return 0, None, [], False, "package_hash_mismatch"
        if data.get("diff_hash") != diff_hash:
            return 0, None, [], False, "diff_hash_mismatch"

        iteration = int(data.get("iteration", 0))
        if iteration <= 0:
            return 0, None, [], False, "checkpoint_empty"
        if iteration >= max(1, self.max_iter):
            return 0, None, [], False, "checkpoint_complete"

        self.run_id = str(data.get("run_id") or self.run_id)
        records = [
            _iteration_record_from_dict(item)
            for item in data.get("iterations", [])
        ]
        feedback_data = data.get("last_feedback")
        prior_feedback = (
            _prior_feedback_from_dict(feedback_data)
            if isinstance(feedback_data, dict)
            else None
        )
        return iteration, prior_feedback, records, True, None

    def _save_checkpoint(
        self,
        records: list[IterationRecord],
        *,
        next_feedback: PriorFeedback | None,
        converged: bool,
        package_hash: str,
        diff_hash: str,
    ) -> None:
        if self.out_dir is None:
            return
        self.out_dir.mkdir(parents=True, exist_ok=True)
        if not self.run_id:
            self.run_id = uuid4().hex
        data = {
            "schema_version": LOOP_SCHEMA_VERSION,
            "run_id": self.run_id,
            "mode": self.mode,
            "max_iter": max(1, self.max_iter),
            "iteration": len(records),
            "converged": converged,
            "package_hash": package_hash,
            "diff_hash": diff_hash,
            "iterations": [record.to_dict() for record in records],
            "last_feedback": (
                next_feedback.to_dict() if next_feedback is not None else None
            ),
        }
        (self.out_dir / LOOP_CHECKPOINT_FILENAME).write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _checkpoint_path_str(self) -> str | None:
        if self.out_dir is None:
            return None
        return str(self.out_dir / LOOP_CHECKPOINT_FILENAME)


def _converged(records: list[IterationRecord], critique: CritiqueResult) -> bool:
    if not critique.uncertain:
        return True
    if len(records) >= 2 and records[-1].issue_set == records[-2].issue_set:
        return True
    return False


def _normalized_issue_set(critique: CritiqueResult) -> list[str]:
    ids = [_issue_id(issue) for issue in critique.keep]
    ids.extend(item.issue_id for item in critique.uncertain)
    ids.extend(_issue_id(issue) for issue in critique.reject)
    return sorted(dict.fromkeys(ids))


def _issues_for_feedback(
    feedback_items: list[UncertainFeedbackItem],
    issues: list[ReviewIssue],
) -> list[ReviewIssue]:
    feedback_ids = {item.issue_id for item in feedback_items}
    return [issue for issue in issues if _issue_id(issue) in feedback_ids]


def _agent_runs_for_iteration(
    *,
    i: int,
    feedback_hash: str,
    reviewer: ReviewAgent,
    critic: CriticAgent,
    package: EvidencePackage,
    candidates: list[ReviewIssue],
    verified: list[ReviewIssue],
    critique: CritiqueResult,
) -> list[AgentRun]:
    reviewer_run_list = getattr(reviewer, "last_agent_runs", None)
    reviewer_run = getattr(reviewer, "last_agent_run", None)
    if (
        isinstance(reviewer_run_list, list)
        and reviewer_run_list
        and all(isinstance(run, AgentRun) for run in reviewer_run_list)
    ):
        reviewer_runs = [
            _with_iteration(run, iteration=i, feedback_hash=feedback_hash)
            for run in reviewer_run_list
        ]
    elif isinstance(reviewer_run, AgentRun):
        reviewer_runs = [
            _with_iteration(reviewer_run, iteration=i, feedback_hash=feedback_hash)
        ]
    else:
        reviewer_runs = [
            AgentRun(
                agent_name=_agent_name(reviewer, "reviewer"),
                model=getattr(reviewer, "model", None),
                prompt_hash=_safe_prompt_hash("review_agent.md"),
                input_evidence_ids=sorted(package.evidence_index),
                output_issue_ids=[_issue_id(issue) for issue in candidates],
                iteration=i,
                feedback_hash=feedback_hash,
            )
        ]

    if critique.agent_runs:
        return [
            *reviewer_runs,
            *[
            _with_iteration(run, iteration=i, feedback_hash=feedback_hash)
            for run in critique.agent_runs
            ],
        ]

    return [
        *reviewer_runs,
        AgentRun(
            agent_name=_agent_name(critic, "critic"),
            model=getattr(critic, "model", None),
            prompt_hash=_safe_prompt_hash("critic_agent.md"),
            input_evidence_ids=sorted(
                {
                    evidence_id
                    for issue in verified
                    for evidence_id in issue.evidence_ids
                }
            ),
            output_issue_ids=[_issue_id(issue) for issue in critique.keep],
            iteration=i,
            feedback_hash=feedback_hash,
        ),
    ]


def _with_iteration(
    run: AgentRun, *, iteration: int, feedback_hash: str
) -> AgentRun:
    return AgentRun(
        agent_name=run.agent_name,
        model=run.model,
        prompt_hash=run.prompt_hash,
        input_evidence_ids=list(run.input_evidence_ids),
        output_issue_ids=list(run.output_issue_ids),
        fallback_used=run.fallback_used,
        iteration=iteration,
        feedback_hash=feedback_hash,
        retry_count=run.retry_count,
        retry_log=list(run.retry_log),
        latency_ms=run.latency_ms,
        token_count_in=run.token_count_in,
        token_count_out=run.token_count_out,
        trace_id=run.trace_id,
        span_id=run.span_id,
        parent_span_id=run.parent_span_id,
        status=run.status,
        error_type=run.error_type,
        shard_id=run.shard_id,
        shard_index=run.shard_index,
        shard_count=run.shard_count,
        context_request_count=run.context_request_count,
        context_refill_used=run.context_refill_used,
    )


def _all_agent_runs(records: list[IterationRecord]) -> list[AgentRun]:
    return [run for record in records for run in record.agent_runs]


def _exclude_final(
    needs_human_review: list[ReviewIssue],
    final_issues: list[ReviewIssue],
) -> list[ReviewIssue]:
    """Remove issues from needs_human_review that already appear in final_issues."""
    final_ids = {_issue_id(issue) for issue in final_issues}
    return [issue for issue in needs_human_review if _issue_id(issue) not in final_ids]


def _merge_duplicates(issues: list[ReviewIssue]) -> list[ReviewIssue]:
    seen: dict[tuple[str, str], ReviewIssue] = {}
    for issue in issues:
        key = (issue.file, issue.category)
        existing = seen.get(key)
        if existing is None:
            seen[key] = issue
            continue
        if issue.confidence > existing.confidence:
            seen[key] = issue
    return list(seen.values())


def _feedback_hash(feedback: PriorFeedback | None) -> str:
    if feedback is None:
        return ""
    raw = json.dumps(feedback.to_dict(), sort_keys=True, ensure_ascii=False)
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _stable_hash(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False)
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _safe_prompt_hash(prompt_name: str) -> str:
    try:
        return prompt_hash(prompt_name)
    except FileNotFoundError:
        return ""


def _agent_name(agent: object, suffix: str) -> str:
    strategy = getattr(agent, "strategy", "")
    if strategy:
        return f"{agent.__class__.__name__}:{strategy}"
    return f"{agent.__class__.__name__}:{suffix}"


def _issue_id(issue: ReviewIssue) -> str:
    line = issue.line if issue.line is not None else "?"
    return f"{issue.category}:{issue.file}:{line}"


def _iteration_record_from_dict(data: dict[str, Any]) -> IterationRecord:
    return IterationRecord(
        i=int(data.get("i", 0)),
        candidate_issue_count=int(data.get("candidate_issue_count", 0)),
        verified_count=int(data.get("verified_count", 0)),
        needs_human_review_count=int(data.get("needs_human_review_count", 0)),
        discarded_count=int(data.get("discarded_count", 0)),
        keep_count=int(data.get("keep_count", 0)),
        uncertain_count=int(data.get("uncertain_count", 0)),
        reject_count=int(data.get("reject_count", 0)),
        feedback_sent=[
            _feedback_item_from_dict(item)
            for item in data.get("feedback_sent", [])
            if isinstance(item, dict)
        ],
        agent_runs=[
            _agent_run_from_dict(item)
            for item in data.get("agent_runs", [])
            if isinstance(item, dict)
        ],
        issue_set=[str(item) for item in data.get("issue_set", [])],
        keep=[
            _review_issue_from_dict(item)
            for item in data.get("keep", [])
            if isinstance(item, dict)
        ],
        needs_human_review=[
            _review_issue_from_dict(item)
            for item in data.get("needs_human_review", [])
            if isinstance(item, dict)
        ],
        discarded=[
            _discarded_from_dict(item)
            for item in data.get("discarded", [])
            if isinstance(item, dict)
        ],
    )


def _prior_feedback_from_dict(data: dict[str, Any]) -> PriorFeedback:
    return PriorFeedback(
        iteration=int(data.get("iteration", 0)),
        uncertain_items=[
            _feedback_item_from_dict(item)
            for item in data.get("uncertain_items", [])
            if isinstance(item, dict)
        ],
    )


def _feedback_item_from_dict(data: dict[str, Any]) -> UncertainFeedbackItem:
    return UncertainFeedbackItem(
        issue_id=str(data.get("issue_id", "")),
        category=str(data.get("category", "")),
        critic_reason=str(data.get("critic_reason", "")),
        original_confidence=_float(data.get("original_confidence", 0.0)),
        evidence_ids=[str(item) for item in data.get("evidence_ids", [])],
    )


def _agent_run_from_dict(data: dict[str, Any]) -> AgentRun:
    return AgentRun(
        agent_name=str(data.get("agent_name", "")),
        model=_optional_str(data.get("model")),
        prompt_hash=_optional_str(data.get("prompt_hash")),
        input_evidence_ids=[
            str(item) for item in data.get("input_evidence_ids", [])
        ],
        output_issue_ids=[str(item) for item in data.get("output_issue_ids", [])],
        fallback_used=bool(data.get("fallback_used", False)),
        iteration=int(data.get("iteration", 0)),
        feedback_hash=str(data.get("feedback_hash", "")),
        retry_count=int(data.get("retry_count", 0)),
        retry_log=[str(item) for item in data.get("retry_log", [])],
        latency_ms=int(data.get("latency_ms", 0)),
        token_count_in=int(data.get("token_count_in", 0)),
        token_count_out=int(data.get("token_count_out", 0)),
        trace_id=str(data.get("trace_id", "")),
        span_id=str(data.get("span_id", "")),
        parent_span_id=str(data.get("parent_span_id", "")),
        status=str(data.get("status", "ok")),
        error_type=str(data.get("error_type", "")),
        shard_id=str(data.get("shard_id", "")),
        shard_index=int(data.get("shard_index", 0)),
        shard_count=int(data.get("shard_count", 0)),
        context_request_count=int(data.get("context_request_count", 0)),
        context_refill_used=bool(data.get("context_refill_used", False)),
    )


def _discarded_from_dict(data: dict[str, Any]) -> GroundingDiscardedIssue:
    return GroundingDiscardedIssue(
        issue=_review_issue_from_dict(data),
        reason=str(data.get("filter_reason", data.get("reason", ""))),
    )


def _review_issue_from_dict(data: dict[str, Any]) -> ReviewIssue:
    return ReviewIssue(
        file=str(data.get("file", "patch")),
        line=_optional_int(data.get("line")),
        severity=str(data.get("severity", "medium")),
        category=str(data.get("category", "unknown")),
        message=str(data.get("message", "")),
        suggestion=str(data.get("suggestion", "")),
        confidence=_float(data.get("confidence", 0.0)),
        evidence_ids=[str(item) for item in data.get("evidence_ids", [])],
    )


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
