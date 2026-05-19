"""Fake review agents used to exercise the evidence-first harness."""

from __future__ import annotations

import ast
import hashlib
import http.client
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol
from urllib import error, request
from uuid import uuid4

from code_review_agent.models import (
    AgentRun,
    ContextRequest,
    CritiqueResult,
    EvidencePackage,
    PriorFeedback,
    ReviewerContext,
    ReviewIssue,
    RiskSignal,
    UncertainFeedbackItem,
)
from code_review_agent.review.context_budget import (
    DEFAULT_CONTEXT_BUDGET_TOKENS,
    DEFAULT_MAX_EVIDENCE_PER_FILE,
    DEFAULT_MAX_FILES_PER_AGENT_CALL,
    aggregate_context_budget,
    build_context_refill,
    build_reviewer_contexts,
)
from code_review_agent.review.risk import DOC_ONLY, risk_evidence_id


RECALL_BIASED_REVIEWER = "recall_biased_reviewer"
PRECISION_BIASED_CRITIC = "precision_biased_critic"
SAME_STRATEGY = "same_strategy"
CROSS_STRATEGY = "cross_strategy"
FAKE_MODEL_NAME = "fake-llm"
DEFAULT_OPENAI_COMPATIBLE_BASE_URL = "https://api.siliconflow.cn/v1"
DEFAULT_OPENAI_COMPATIBLE_MODEL = "deepseek-ai/DeepSeek-V4-Flash"
OPENAI_COMPATIBLE_TIMEOUT_SECONDS = 60
RETRYABLE_HTTP_STATUS_CODES = frozenset({429, 500, 502, 503, 504})
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_BACKOFF_SECONDS = 1.0
LIVE_CONTEXT_CHECKPOINT_SCHEMA_VERSION = "live_context_checkpoint_v1"
ALLOWED_CONTEXT_REQUEST_TYPES = frozenset(
    {
        "same_file_more_evidence",
        "related_tests",
        "related_symbol",
        "risk_evidence",
    }
)

_PROMPT_DIR = Path(__file__).with_name("prompts")
_REVIEW_PROMPT = "review_agent.md"
_CRITIC_PROMPT = "critic_agent.md"


class _AgentFatalError(RuntimeError):
    """Non-retryable agent failure."""


class _AgentTransientError(RuntimeError):
    """Retryable agent failure that exhausted all attempts."""


class ReviewAgent(Protocol):
    def review(
        self,
        package: EvidencePackage,
        *,
        prior_feedback: PriorFeedback | None = None,
    ) -> list[ReviewIssue]:
        """Return candidate review issues for one evidence package."""


class CriticAgent(Protocol):
    def critique(
        self, issues: list[ReviewIssue], package: EvidencePackage
    ) -> CritiqueResult:
        """Return structured critic decisions for candidate issues."""


@dataclass(slots=True)
class FakeAgentResult:
    """Outputs from the fake reviewer/critic pair."""

    findings: list[ReviewIssue] = field(default_factory=list)
    needs_human_review: list[ReviewIssue] = field(default_factory=list)
    agent_runs: list[AgentRun] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "findings": [issue.to_dict() for issue in self.findings],
            "needs_human_review": [
                issue.to_dict() for issue in self.needs_human_review
            ],
            "agent_runs": [run.to_dict() for run in self.agent_runs],
        }


@dataclass(slots=True)
class FakeLLMReviewAgent:
    """Recall-biased fake reviewer that proposes evidence-linked candidates."""

    strategy: str = RECALL_BIASED_REVIEWER

    def review(
        self,
        package: EvidencePackage,
        *,
        prior_feedback: PriorFeedback | None = None,
    ) -> list[ReviewIssue]:
        if self.strategy == PRECISION_BIASED_CRITIC:
            issues = [
                issue
                for issue in _issues_from_risk_signals(package)
                if issue.confidence >= 0.75
            ]
            return _apply_prior_feedback(issues, prior_feedback)

        issues = _issues_from_risk_signals(package)
        invalid = _invalid_evidence_probe(package)
        if invalid is not None:
            issues.append(invalid)
        return _apply_prior_feedback(issues, prior_feedback)


@dataclass(slots=True)
class FakeLLMCriticAgent:
    """Precision-biased fake critic that downgrades weak candidates."""

    strategy: str = PRECISION_BIASED_CRITIC

    def filter(
        self, issues: list[ReviewIssue], package: EvidencePackage
    ) -> list[ReviewIssue]:
        critique = self.critique(issues, package)
        uncertain_ids = {item.issue_id for item in critique.uncertain}
        uncertain_issues = [
            _downgrade_uncertain_issue(issue)
            for issue in issues
            if _issue_id(issue) in uncertain_ids
        ]
        return [*critique.keep, *uncertain_issues]

    def critique(
        self, issues: list[ReviewIssue], package: EvidencePackage
    ) -> CritiqueResult:
        if self.strategy == RECALL_BIASED_REVIEWER:
            return CritiqueResult(keep=list(issues))

        keep: list[ReviewIssue] = []
        uncertain: list[UncertainFeedbackItem] = []
        reject: list[ReviewIssue] = []
        for issue in issues:
            if _looks_like_style_nit(issue):
                reject.append(issue)
                continue
            if not any(eid in package.evidence_index for eid in issue.evidence_ids):
                uncertain.append(
                    _feedback_item(issue, "ungrounded evidence")
                )
                continue
            if issue.category in {"api_change", "behavior_change", "security_sensitive"}:
                uncertain.append(
                    _feedback_item(issue, "requires semantic confirmation")
                )
                continue
            if issue.confidence < 0.6:
                uncertain.append(_feedback_item(issue, "low confidence"))
                continue
            keep.append(issue)
        return CritiqueResult(keep=keep, uncertain=uncertain, reject=reject)


@dataclass(slots=True)
class OpenAICompatibleReviewAgent:
    """OpenAI-compatible chat-completions reviewer using only stdlib HTTP."""

    api_key: str
    base_url: str = DEFAULT_OPENAI_COMPATIBLE_BASE_URL
    model: str = DEFAULT_OPENAI_COMPATIBLE_MODEL
    timeout_seconds: int = OPENAI_COMPATIBLE_TIMEOUT_SECONDS
    context_budget_tokens: int = DEFAULT_CONTEXT_BUDGET_TOKENS
    max_files_per_agent_call: int = DEFAULT_MAX_FILES_PER_AGENT_CALL
    max_evidence_per_file: int = DEFAULT_MAX_EVIDENCE_PER_FILE
    max_context_refill_rounds: int = 1
    max_context_requests: int = 8
    context_checkpoint_path: str | None = None
    context_checkpoint_package_hash: str = ""
    context_checkpoint_diff_hash: str = ""
    context_checkpoint_resume: bool = False
    last_agent_run: AgentRun | None = field(default=None, init=False, repr=False)
    last_agent_runs: list[AgentRun] = field(default_factory=list, init=False, repr=False)
    last_context_budget: dict | None = field(default=None, init=False, repr=False)
    last_context_requests: list[ContextRequest] = field(
        default_factory=list, init=False, repr=False
    )

    @classmethod
    def from_env(cls) -> "OpenAICompatibleReviewAgent":
        api_key = os.environ.get("SILICONFLOW_API_KEY") or os.environ.get(
            "OPENAI_COMPATIBLE_API_KEY"
        )
        if not api_key:
            raise ValueError(
                "hybrid-live requires SILICONFLOW_API_KEY or "
                "OPENAI_COMPATIBLE_API_KEY in the environment."
            )
        return cls(
            api_key=api_key,
            base_url=os.environ.get(
                "SILICONFLOW_BASE_URL",
                os.environ.get(
                    "OPENAI_COMPATIBLE_BASE_URL",
                    DEFAULT_OPENAI_COMPATIBLE_BASE_URL,
                ),
            ),
            model=os.environ.get(
                "SILICONFLOW_MODEL",
                os.environ.get(
                    "OPENAI_COMPATIBLE_MODEL",
                    DEFAULT_OPENAI_COMPATIBLE_MODEL,
                ),
            ),
        )

    def review(
        self,
        package: EvidencePackage,
        *,
        prior_feedback: PriorFeedback | None = None,
    ) -> list[ReviewIssue]:
        self.last_agent_run = None
        self.last_agent_runs = []
        self.last_context_requests = []
        contexts = build_reviewer_contexts(
            package,
            max_input_tokens=self.context_budget_tokens,
            max_files=self.max_files_per_agent_call,
            max_evidence_per_file=self.max_evidence_per_file,
        )
        reviewed_contexts: list[ReviewerContext] = list(contexts)
        issues: list[ReviewIssue] = []
        failed_primary_contexts = 0
        for context in contexts:
            try:
                shard_issues, context_requests = self._review_context(
                    package,
                    context,
                    prior_feedback=prior_feedback,
                    context_refill_used=False,
                )
            except _AgentTransientError:
                failed_primary_contexts += 1
                continue
            issues.extend(shard_issues)
            self.last_context_requests.extend(context_requests)
            if context_requests and self.max_context_refill_rounds > 0:
                refill_context = build_context_refill(
                    package,
                    context,
                    context_requests,
                    max_input_tokens=self.context_budget_tokens,
                    max_evidence_per_file=self.max_evidence_per_file,
                    max_context_requests=self.max_context_requests,
                )
                if refill_context is not None:
                    reviewed_contexts.append(refill_context)
                    try:
                        refill_issues, refill_requests = self._review_context(
                            package,
                            refill_context,
                            prior_feedback=prior_feedback,
                            context_refill_used=True,
                        )
                    except _AgentTransientError:
                        continue
                    issues.extend(refill_issues)
                    self.last_context_requests.extend(refill_requests)

        self.last_context_budget = aggregate_context_budget(
            reviewed_contexts,
            context_requests=self.last_context_requests,
        )
        if failed_primary_contexts >= len(contexts) and not issues:
            raise _AgentTransientError("All live review context shards failed.")
        return _apply_prior_feedback(_merge_review_issues(issues), prior_feedback)

    def _review_context(
        self,
        package: EvidencePackage,
        context: ReviewerContext,
        *,
        prior_feedback: PriorFeedback | None,
        context_refill_used: bool,
    ) -> tuple[list[ReviewIssue], list[ContextRequest]]:
        checkpoint_key = _context_checkpoint_key(context, prior_feedback)
        restored = self._load_context_checkpoint_item(checkpoint_key)
        if restored is not None:
            issues = [
                _issue_from_dict(item)
                for item in restored.get("issues", [])
                if isinstance(item, dict)
            ]
            context_requests = [
                _context_request_from_dict(item, source_shard_id=context.shard_id)
                for item in restored.get("context_requests", [])
                if isinstance(item, dict)
            ]
            run = _openai_agent_run(
                model=self.model,
                prompt_digest=prompt_hash(_REVIEW_PROMPT),
                package=package,
                input_evidence_ids=sorted(context.evidence_index),
                context_budget=context.context_budget,
                context=context,
                output_issues=issues,
                retry_log=[],
                latency_ms=0,
                token_count_in=0,
                token_count_out=0,
                trace_id=uuid4().hex,
                span_id=uuid4().hex[:16],
                status="resumed",
                error_type="",
                context_request_count=len(context_requests),
                context_refill_used=context_refill_used,
            )
            self.last_agent_run = run
            self.last_agent_runs.append(run)
            return issues, context_requests

        started = time.monotonic()
        retry_log: list[str] = []
        trace_id = uuid4().hex
        span_id = uuid4().hex[:16]
        review_prompt_hash = prompt_hash(_REVIEW_PROMPT)
        selected_evidence_ids = list(context.evidence_index)
        body = _live_review_body(
            model=self.model,
            prior_feedback=prior_feedback,
            context=context,
        )
        try:
            response = _retry_with_backoff(
                lambda: _post_openai_compatible_json(
                    f"{self.base_url.rstrip('/')}/chat/completions",
                    api_key=self.api_key,
                    body=body,
                    timeout_seconds=self.timeout_seconds,
                ),
                retry_log=retry_log,
            )
            content = _chat_completion_text(response)
            issues, context_requests = _review_response_from_llm_json(
                content,
                source_shard_id=context.shard_id,
                max_context_requests=self.max_context_requests,
            )
        except (_AgentFatalError, _AgentTransientError) as exc:
            run = _openai_agent_run(
                model=self.model,
                prompt_digest=review_prompt_hash,
                package=package,
                input_evidence_ids=selected_evidence_ids,
                context_budget=context.context_budget,
                context=context,
                output_issues=[],
                retry_log=retry_log,
                latency_ms=_elapsed_ms(started),
                token_count_in=0,
                token_count_out=0,
                trace_id=trace_id,
                span_id=span_id,
                status="error",
                error_type=exc.__class__.__name__,
                context_request_count=0,
                context_refill_used=context_refill_used,
            )
            self.last_agent_run = run
            self.last_agent_runs.append(run)
            raise
        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            run = _openai_agent_run(
                model=self.model,
                prompt_digest=review_prompt_hash,
                package=package,
                input_evidence_ids=selected_evidence_ids,
                context_budget=context.context_budget,
                context=context,
                output_issues=[],
                retry_log=retry_log,
                latency_ms=_elapsed_ms(started),
                token_count_in=0,
                token_count_out=0,
                trace_id=trace_id,
                span_id=span_id,
                status="error",
                error_type=exc.__class__.__name__,
                context_request_count=0,
                context_refill_used=context_refill_used,
            )
            self.last_agent_run = run
            self.last_agent_runs.append(run)
            raise _AgentTransientError(
                f"OpenAI-compatible reviewer produced invalid output: {exc}"
            ) from exc

        run = _openai_agent_run(
            model=self.model,
            prompt_digest=review_prompt_hash,
            package=package,
            input_evidence_ids=selected_evidence_ids,
            context_budget=context.context_budget,
            context=context,
            output_issues=issues,
            retry_log=retry_log,
            latency_ms=_elapsed_ms(started),
            token_count_in=_usage_tokens(response, "prompt_tokens", "input_tokens"),
            token_count_out=_usage_tokens(
                response, "completion_tokens", "output_tokens"
            ),
            trace_id=trace_id,
            span_id=span_id,
            status="ok",
            error_type="",
            context_request_count=len(context_requests),
            context_refill_used=context_refill_used,
        )
        self.last_agent_run = run
        self.last_agent_runs.append(run)
        self._save_context_checkpoint_item(
            checkpoint_key,
            context=context,
            issues=issues,
            context_requests=context_requests,
            run=run,
        )
        return issues, context_requests

    def _load_context_checkpoint_item(self, key: str) -> dict | None:
        if not self.context_checkpoint_resume or self.context_checkpoint_path is None:
            return None
        path = Path(self.context_checkpoint_path)
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
        if data.get("schema_version") != LIVE_CONTEXT_CHECKPOINT_SCHEMA_VERSION:
            return None
        if data.get("package_hash") != self.context_checkpoint_package_hash:
            return None
        if data.get("diff_hash") != self.context_checkpoint_diff_hash:
            return None
        item = data.get("shards", {}).get(key)
        if not isinstance(item, dict) or item.get("status") != "completed":
            return None
        return item

    def _save_context_checkpoint_item(
        self,
        key: str,
        *,
        context: ReviewerContext,
        issues: list[ReviewIssue],
        context_requests: list[ContextRequest],
        run: AgentRun,
    ) -> None:
        if self.context_checkpoint_path is None:
            return
        path = Path(self.context_checkpoint_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data: dict[str, Any] = {
            "schema_version": LIVE_CONTEXT_CHECKPOINT_SCHEMA_VERSION,
            "package_hash": self.context_checkpoint_package_hash,
            "diff_hash": self.context_checkpoint_diff_hash,
            "shards": {},
        }
        if path.exists():
            try:
                existing: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                existing = {}
            if (
                existing.get("schema_version")
                == LIVE_CONTEXT_CHECKPOINT_SCHEMA_VERSION
                and existing.get("package_hash") == self.context_checkpoint_package_hash
                and existing.get("diff_hash") == self.context_checkpoint_diff_hash
            ):
                data = existing
                data.setdefault("shards", {})
        data["shards"][key] = {
            "status": "completed",
            "shard_id": context.shard_id,
            "is_refill": context.is_refill,
            "parent_shard_id": context.parent_shard_id,
            "selected_evidence_ids": sorted(context.evidence_index),
            "context_requests": [
                context_request.to_dict()
                for context_request in context_requests
            ],
            "issues": [issue.to_dict() for issue in issues],
            "agent_run": run.to_dict(),
        }
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def run_fake_hybrid_agents(
    package: EvidencePackage, *, pair_strategy: str = CROSS_STRATEGY
) -> FakeAgentResult:
    """Run the fake reviewer/critic pair and return candidate issues."""

    reviewer_strategy = RECALL_BIASED_REVIEWER
    critic_strategy = (
        RECALL_BIASED_REVIEWER
        if pair_strategy == SAME_STRATEGY
        else PRECISION_BIASED_CRITIC
    )
    reviewer = FakeLLMReviewAgent(strategy=reviewer_strategy)
    critic = FakeLLMCriticAgent(strategy=critic_strategy)

    candidate_issues = reviewer.review(package)
    criticised_issues = critic.filter(candidate_issues, package)
    input_evidence_ids = sorted(package.evidence_index)
    critic_input_evidence_ids = sorted(
        {
            evidence_id
            for issue in candidate_issues
            for evidence_id in issue.evidence_ids
        }
    )

    return FakeAgentResult(
        findings=criticised_issues,
        agent_runs=[
            AgentRun(
                agent_name=f"fake_reviewer:{reviewer_strategy}",
                model=FAKE_MODEL_NAME,
                prompt_hash=prompt_hash(_REVIEW_PROMPT),
                input_evidence_ids=input_evidence_ids,
                output_issue_ids=[_issue_id(issue) for issue in candidate_issues],
                fallback_used=False,
            ),
            AgentRun(
                agent_name=f"fake_critic:{critic_strategy}",
                model=FAKE_MODEL_NAME,
                prompt_hash=prompt_hash(_CRITIC_PROMPT),
                input_evidence_ids=critic_input_evidence_ids,
                output_issue_ids=[_issue_id(issue) for issue in criticised_issues],
                fallback_used=False,
            ),
        ],
    )


def run_openai_compatible_review_agent(
    package: EvidencePackage,
    *,
    agent: OpenAICompatibleReviewAgent | None = None,
) -> FakeAgentResult:
    """Run a live OpenAI-compatible reviewer and return candidate issues."""

    reviewer = agent or OpenAICompatibleReviewAgent.from_env()
    issues = reviewer.review(package)
    live_run = getattr(reviewer, "last_agent_run", None)
    if isinstance(live_run, AgentRun):
        agent_runs = [live_run]
    else:
        agent_runs = [
            AgentRun(
                agent_name="openai_compatible_reviewer",
                model=reviewer.model,
                prompt_hash=prompt_hash(_REVIEW_PROMPT),
                input_evidence_ids=sorted(package.evidence_index),
                output_issue_ids=[_issue_id(issue) for issue in issues],
                fallback_used=False,
            )
        ]
    return FakeAgentResult(
        findings=issues,
        agent_runs=agent_runs,
    )


def export_agent_prompts(
    package: EvidencePackage,
    out_dir: Path | str,
    *,
    mode: str,
    pair_strategy: str = CROSS_STRATEGY,
    context_budget_tokens: int = DEFAULT_CONTEXT_BUDGET_TOKENS,
    max_files_per_agent_call: int = DEFAULT_MAX_FILES_PER_AGENT_CALL,
    max_evidence_per_file: int = DEFAULT_MAX_EVIDENCE_PER_FILE,
) -> dict:
    """Export prompt templates and redacted agent inputs for demos."""

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    review_hash = prompt_hash(_REVIEW_PROMPT)
    critic_hash = prompt_hash(_CRITIC_PROMPT)
    review_prompt_path = out / "review_agent_prompt.md"
    critic_prompt_path = out / "critic_agent_prompt.md"
    review_input_path = out / "review_agent_input.json"
    critic_input_path = out / "critic_agent_input.json"

    review_prompt_path.write_text(
        _render_prompt_export(_REVIEW_PROMPT, review_hash),
        encoding="utf-8",
    )
    critic_prompt_path.write_text(
        _render_prompt_export(_CRITIC_PROMPT, critic_hash),
        encoding="utf-8",
    )
    review_input = {
        "mode": mode,
        "pair_strategy": pair_strategy,
        "prompt_hash": review_hash,
        "redacted_metadata_fields": package.metadata.get("redacted", []),
    }
    if mode.startswith("hybrid-live"):
        reviewer_contexts = build_reviewer_contexts(
            package,
            max_input_tokens=context_budget_tokens,
            max_files=max_files_per_agent_call,
            max_evidence_per_file=max_evidence_per_file,
        )
        review_input["reviewer_contexts"] = [
            _llm_context_payload(context) for context in reviewer_contexts
        ]
        review_input["live_review_input"] = _llm_context_payload(reviewer_contexts[0])
        review_input["context_budget"] = aggregate_context_budget(reviewer_contexts)
        review_input["full_package_exported"] = False
    else:
        review_input["package"] = package.to_dict()
        review_input["full_package_exported"] = True

    review_input_path.write_text(
        json.dumps(review_input, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    critic_input_path.write_text(
        json.dumps(
            {
                "mode": mode,
                "pair_strategy": pair_strategy,
                "prompt_hash": critic_hash,
                "candidate_issue_contract": "list[ReviewIssue]",
                "evidence_ids": sorted(package.evidence_index),
                "redacted_metadata_fields": package.metadata.get("redacted", []),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return {
        "directory": str(out),
        "review_prompt_hash": review_hash,
        "critic_prompt_hash": critic_hash,
        "files": [
            str(review_input_path),
            str(review_prompt_path),
            str(critic_input_path),
            str(critic_prompt_path),
        ],
    }


def prompt_hash(prompt_name: str) -> str:
    content = _load_prompt(prompt_name)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _post_openai_compatible_json(
    url: str,
    *,
    api_key: str,
    body: dict,
    timeout_seconds: int,
) -> dict:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with request.urlopen(req, timeout=timeout_seconds) as response:
        raw = response.read().decode("utf-8", errors="replace")
    result: dict[str, Any] = json.loads(raw)
    return result


def _retry_with_backoff(
    call,
    *,
    retry_log: list[str],
    max_attempts: int = DEFAULT_RETRY_ATTEMPTS,
    base_delay_seconds: float = DEFAULT_BACKOFF_SECONDS,
) -> dict:
    attempts = max(1, max_attempts)
    for attempt in range(1, attempts + 1):
        try:
            result: dict[str, Any] = call()
            return result
        except error.HTTPError as exc:
            if exc.code not in RETRYABLE_HTTP_STATUS_CODES:
                raise _AgentFatalError(
                    f"OpenAI-compatible API returned HTTP {exc.code}: "
                    f"{_truncate(_error_body(exc))}"
                ) from exc
            if attempt >= attempts:
                raise _AgentTransientError(
                    f"OpenAI-compatible API returned HTTP {exc.code} after "
                    f"{attempts} attempts."
                ) from exc
            delay = _retry_delay_seconds(exc, attempt, base_delay_seconds)
            retry_log.append(f"attempt={attempt} error=http_{exc.code} delay={delay:.2f}s")
            time.sleep(delay)
        except error.URLError as exc:
            if attempt >= attempts:
                raise _AgentTransientError(
                    f"OpenAI-compatible API request failed after {attempts} attempts: "
                    f"{exc.reason}"
                ) from exc
            delay = base_delay_seconds * (2 ** (attempt - 1))
            retry_log.append(f"attempt={attempt} error=url_error delay={delay:.2f}s")
            time.sleep(delay)
        except (ConnectionError, http.client.RemoteDisconnected, TimeoutError) as exc:
            if attempt >= attempts:
                error_name = _transport_error_name(exc)
                raise _AgentTransientError(
                    "OpenAI-compatible API transport failed after "
                    f"{attempts} attempts: {error_name}."
                ) from exc
            delay = base_delay_seconds * (2 ** (attempt - 1))
            retry_log.append(
                "attempt="
                f"{attempt} error={_transport_error_name(exc)} delay={delay:.2f}s"
            )
            time.sleep(delay)

    raise _AgentTransientError(
        f"OpenAI-compatible API request failed after {attempts} attempts."
    )


def _retry_delay_seconds(
    exc: error.HTTPError, attempt: int, base_delay_seconds: float
) -> float:
    retry_after = _retry_after_seconds(getattr(exc, "headers", None))
    if retry_after is not None:
        return float(retry_after)
    return float(base_delay_seconds * (2 ** (attempt - 1)))


def _transport_error_name(exc: BaseException) -> str:
    if isinstance(exc, TimeoutError):
        return "timeout"
    if isinstance(exc, http.client.RemoteDisconnected):
        return "remote_disconnected"
    return exc.__class__.__name__.lower()


def _retry_after_seconds(headers) -> float | None:
    raw = headers.get("Retry-After") if headers is not None else None
    if raw is None:
        return None
    try:
        return max(0.0, float(raw))
    except (TypeError, ValueError):
        return None


def _error_body(exc: error.HTTPError) -> str:
    try:
        return exc.read().decode("utf-8", errors="replace")
    except Exception:
        return ""


def _openai_agent_run(
    *,
    model: str,
    prompt_digest: str,
    package: EvidencePackage,
    input_evidence_ids: list[str],
    context_budget: dict,
    context: ReviewerContext,
    output_issues: list[ReviewIssue],
    retry_log: list[str],
    latency_ms: int,
    token_count_in: int,
    token_count_out: int,
    trace_id: str,
    span_id: str,
    status: str,
    error_type: str,
    context_request_count: int,
    context_refill_used: bool,
) -> AgentRun:
    del package, context_budget
    return AgentRun(
        agent_name="openai_compatible_reviewer",
        model=model,
        prompt_hash=prompt_digest,
        input_evidence_ids=sorted(input_evidence_ids),
        output_issue_ids=[_issue_id(issue) for issue in output_issues],
        retry_count=len(retry_log),
        retry_log=list(retry_log),
        latency_ms=latency_ms,
        token_count_in=token_count_in,
        token_count_out=token_count_out,
        trace_id=trace_id,
        span_id=span_id,
        status=status,
        error_type=error_type,
        shard_id=context.shard_id,
        shard_index=context.shard_index,
        shard_count=context.shard_count,
        context_request_count=context_request_count,
        context_refill_used=context_refill_used,
    )


def _elapsed_ms(started: float) -> int:
    return max(0, round((time.monotonic() - started) * 1000))


def _usage_tokens(response: dict, *keys: str) -> int:
    usage = response.get("usage", {})
    if not isinstance(usage, dict):
        return 0
    for key in keys:
        value = usage.get(key)
        if value is None:
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0
    return 0


def _live_review_body(
    *,
    model: str,
    prior_feedback: PriorFeedback | None,
    context: ReviewerContext,
) -> dict:
    return {
        "model": model,
        "temperature": 0,
        "max_tokens": 4000,
        "messages": [
            {
                "role": "system",
                "content": _load_prompt(_REVIEW_PROMPT),
            },
            {
                "role": "user",
                "content": (
                    "Return only compact valid JSON, with no markdown fences "
                    "or explanatory prose. Prefer an object with keys "
                    "`issues` and `context_requests`; a plain issue array is "
                    "also accepted for compatibility. "
                    "Use only evidence_ids present in "
                    "reviewer_context.evidence_index. "
                    "The available_context manifest lists additional evidence "
                    "you may request if the primary evidence is insufficient. "
                    "Request at most controlled context types: "
                    "same_file_more_evidence, related_tests, related_symbol, "
                    "risk_evidence.\n\n"
                    f"PriorFeedback:\n{_feedback_payload(prior_feedback)}\n\n"
                    "ReviewerContext:\n"
                    f"{json.dumps(_llm_context_payload(context), ensure_ascii=False)}"
                ),
            },
        ],
    }


def _llm_context_payload(context: ReviewerContext) -> dict:
    """Return the compact context view sent to the live reviewer."""

    payload = context.to_dict()
    payload.pop("context_budget", None)
    return payload


def _feedback_payload(prior_feedback: PriorFeedback | None) -> str:
    if prior_feedback is None:
        return "null"
    return json.dumps(prior_feedback.to_dict(), ensure_ascii=False)


def _context_checkpoint_key(
    context: ReviewerContext,
    prior_feedback: PriorFeedback | None,
) -> str:
    payload = {
        "shard_id": context.shard_id,
        "is_refill": context.is_refill,
        "parent_shard_id": context.parent_shard_id,
        "evidence_ids": sorted(context.evidence_index),
        "feedback": (
            prior_feedback.to_dict() if prior_feedback is not None else None
        ),
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _chat_completion_text(response: dict[str, Any]) -> str:
    try:
        text: str = response["choices"][0]["message"]["content"]
        return text
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("OpenAI-compatible response missing choices[0].message.content") from exc


def _issues_from_llm_json(content: str) -> list[ReviewIssue]:
    issues, _ = _review_response_from_llm_json(
        content,
        source_shard_id="",
        max_context_requests=0,
    )
    return issues


def _review_response_from_llm_json(
    content: str,
    *,
    source_shard_id: str,
    max_context_requests: int,
) -> tuple[list[ReviewIssue], list[ContextRequest]]:
    parsed = _loads_llm_json(_extract_json_value(content))
    if not isinstance(parsed, list):
        if not isinstance(parsed, dict):
            raise ValueError("LLM review output must be an object or array.")
        issues_data = parsed.get("issues", [])
        requests_data = parsed.get("context_requests", [])
        if not isinstance(issues_data, list):
            raise ValueError("LLM review output issues must be a JSON array.")
        if not isinstance(requests_data, list):
            raise ValueError("LLM context_requests must be a JSON array.")
        return (
            _issues_from_items(issues_data),
            _context_requests_from_items(
                requests_data,
                source_shard_id=source_shard_id,
                max_context_requests=max_context_requests,
            ),
        )
    return _issues_from_items(parsed), []


def _issues_from_items(items: list) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            issues.append(_issue_from_dict(item))
        except (TypeError, ValueError):
            continue
    return issues


def _context_requests_from_items(
    items: list,
    *,
    source_shard_id: str,
    max_context_requests: int,
) -> list[ContextRequest]:
    requests: list[ContextRequest] = []
    for item in items:
        if len(requests) >= max(0, max_context_requests):
            break
        if not isinstance(item, dict):
            continue
        try:
            requests.append(
                _context_request_from_dict(item, source_shard_id=source_shard_id)
            )
        except ValueError:
            continue
    return requests


def _extract_json_array(content: str) -> str:
    extracted = _extract_json_value(content)
    if not extracted.lstrip().startswith("["):
        raise ValueError("LLM review output did not contain a JSON array.")
    return extracted


def _extract_json_value(content: str) -> str:
    stripped = content.strip()
    if stripped.startswith("```"):
        stripped = stripped.removeprefix("```json").removeprefix("```").strip()
        if "```" in stripped:
            stripped = stripped.split("```", 1)[0].strip()
    array_start = stripped.find("[")
    object_start = stripped.find("{")
    starts = [item for item in [array_start, object_start] if item != -1]
    if not starts:
        raise ValueError("LLM review output did not contain JSON.")
    start = min(starts)
    end = _balanced_json_end(stripped, start)
    if end is None:
        raise ValueError("LLM review output did not contain a complete JSON value.")
    return stripped[start:end]


def _loads_llm_json(raw: str) -> object:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            return _literal_eval_jsonish(raw)
        except (SyntaxError, ValueError) as exc:
            raise json.JSONDecodeError(str(exc), raw, 0) from exc


def _literal_eval_jsonish(raw: str) -> object:
    """Parse Python-literal shaped model output with JSON constants."""

    expression = ast.parse(raw, mode="eval")
    expression = _JsonishConstantTransformer().visit(expression)
    ast.fix_missing_locations(expression)
    return ast.literal_eval(expression)


class _JsonishConstantTransformer(ast.NodeTransformer):
    """Allow common JSON constants in otherwise Python-literal output."""

    _CONSTANTS = {
        "true": True,
        "false": False,
        "null": None,
    }

    def visit_Name(self, node: ast.Name) -> ast.AST:  # noqa: N802 - ast API name.
        lowered = node.id.lower()
        if lowered in self._CONSTANTS:
            return ast.copy_location(ast.Constant(self._CONSTANTS[lowered]), node)
        return node


def _balanced_json_end(text: str, start: int) -> int | None:
    stack: list[str] = []
    quote_char: str | None = None
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if quote_char is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote_char:
                quote_char = None
            continue

        if char in {"'", '"'}:
            quote_char = char
            continue
        if char in "{[":
            stack.append("}" if char == "{" else "]")
            continue
        if char in "}]":
            if not stack or stack[-1] != char:
                return None
            stack.pop()
            if not stack:
                return index + 1
    return None


def _issue_from_dict(data: dict) -> ReviewIssue:
    if not isinstance(data, dict):
        raise ValueError("Each LLM review item must be an object.")
    return ReviewIssue(
        file=str(data.get("file", "patch")),
        line=_optional_int(data.get("line")),
        severity=str(data.get("severity", "medium")),
        category=str(data.get("category", "llm_candidate")),
        message=str(data.get("message", "")).strip(),
        suggestion=str(data.get("suggestion", "")).strip(),
        confidence=_confidence(data.get("confidence", 0.5)),
        evidence_ids=[str(item) for item in data.get("evidence_ids", [])],
    )


def _context_request_from_dict(
    data: dict,
    *,
    source_shard_id: str,
) -> ContextRequest:
    request_type = str(
        data.get("request_type", data.get("type", "same_file_more_evidence"))
    )
    if request_type not in ALLOWED_CONTEXT_REQUEST_TYPES:
        raise ValueError(f"Unsupported context request type: {request_type}")
    evidence_ids = data.get("evidence_ids", [])
    if not isinstance(evidence_ids, list):
        evidence_ids = []
    return ContextRequest(
        request_type=request_type,
        path=_optional_str(data.get("path")),
        evidence_ids=[str(item) for item in evidence_ids[:20]],
        risk_tag=_optional_str(data.get("risk_tag")),
        symbol=_optional_str(data.get("symbol")),
        reason=str(data.get("reason", ""))[:500],
        source_shard_id=source_shard_id,
    )


def _optional_int(value) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _confidence(value) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return 0.5
    return min(max(confidence, 0.0), 1.0)


def _optional_str(value) -> str | None:
    if value is None:
        return None
    return str(value)


def _truncate(text: str, limit: int = 240) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return f"{compact[:limit]}..."


def _issues_from_risk_signals(package: EvidencePackage) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []
    for signal in package.risk_signals:
        if signal.tag == DOC_ONLY:
            continue
        path, line = _first_location(signal, package)
        evidence_ids = _issue_evidence_ids(signal, package)
        if not evidence_ids:
            continue
        issues.append(
            ReviewIssue(
                file=path,
                line=line,
                severity=_severity_for_signal(signal),
                category=signal.tag,
                message=f"Fake reviewer candidate: {signal.reason}",
                suggestion="Validate the evidence and decide whether this risk is actionable.",
                confidence=max(min(signal.confidence - 0.03, 0.9), 0.5),
                evidence_ids=evidence_ids,
            )
        )
    return issues


def _invalid_evidence_probe(package: EvidencePackage) -> ReviewIssue | None:
    for signal in package.risk_signals:
        if signal.tag == DOC_ONLY:
            continue
        path, line = _first_location(signal, package)
        return ReviewIssue(
            file=path,
            line=line,
            severity="low",
            category="fake_unverified_candidate",
            message="Fake reviewer candidate with an intentionally invalid evidence id.",
            suggestion="The deterministic filter should discard this candidate.",
            confidence=0.72,
            evidence_ids=["fake:invalid:evidence"],
        )
    return None


def _issue_evidence_ids(signal: RiskSignal, package: EvidencePackage) -> list[str]:
    evidence_ids = list(signal.evidence_ids)
    signal_evidence_id = risk_evidence_id(signal)
    if signal_evidence_id in package.evidence_index:
        evidence_ids.append(signal_evidence_id)
    return sorted(dict.fromkeys(evidence_ids))


def _first_location(
    signal: RiskSignal, package: EvidencePackage
) -> tuple[str, int | None]:
    for evidence_id in signal.evidence_ids:
        parts = evidence_id.split(":")
        if len(parts) >= 3 and parts[0] in {"diff", "diff_hunk"}:
            line = int(parts[-1]) if parts[-1].isdigit() else None
            return ":".join(parts[1:-1]), line
        if len(parts) >= 3 and parts[0] == "entity":
            return parts[1], None

    for change in package.changed_files:
        path = change.new_path or change.old_path
        if path is not None:
            return path, None
    return "patch", None


def _severity_for_signal(signal: RiskSignal) -> str:
    if signal.tag in {"security_sensitive", "api_change"}:
        return "medium"
    if signal.tag in {"dependency_change", "config_change"}:
        return "low"
    return "medium"


def _with_confidence(issue: ReviewIssue, confidence: float) -> ReviewIssue:
    return ReviewIssue(
        file=issue.file,
        line=issue.line,
        severity=issue.severity,
        category=issue.category,
        message=issue.message,
        suggestion=issue.suggestion,
        confidence=confidence,
        evidence_ids=list(issue.evidence_ids),
    )


def _apply_prior_feedback(
    issues: list[ReviewIssue],
    prior_feedback: PriorFeedback | None,
) -> list[ReviewIssue]:
    if prior_feedback is None or not prior_feedback.uncertain_items:
        return issues

    uncertain_ids = {item.issue_id for item in prior_feedback.uncertain_items}
    revised: list[ReviewIssue] = []
    for issue in issues:
        if _issue_id(issue) not in uncertain_ids:
            revised.append(issue)
            continue
        revised.append(_with_confidence(issue, issue.confidence * 0.8))
    return revised


def _merge_review_issues(issues: list[ReviewIssue]) -> list[ReviewIssue]:
    seen: dict[tuple[str, str, int | None], ReviewIssue] = {}
    for issue in issues:
        key = (issue.category, issue.file, issue.line)
        existing = seen.get(key)
        if existing is None:
            seen[key] = issue
            continue
        winner = existing if existing.confidence >= issue.confidence else issue
        evidence_ids = sorted(dict.fromkeys(existing.evidence_ids + issue.evidence_ids))
        seen[key] = ReviewIssue(
            file=winner.file,
            line=winner.line,
            severity=winner.severity,
            category=winner.category,
            message=winner.message,
            suggestion=winner.suggestion,
            confidence=max(existing.confidence, issue.confidence),
            evidence_ids=evidence_ids,
        )
    return list(seen.values())


def _feedback_item(issue: ReviewIssue, reason: str) -> UncertainFeedbackItem:
    return UncertainFeedbackItem(
        issue_id=_issue_id(issue),
        category=issue.category,
        critic_reason=reason,
        original_confidence=issue.confidence,
        evidence_ids=list(issue.evidence_ids),
    )


def _downgrade_uncertain_issue(issue: ReviewIssue) -> ReviewIssue:
    if not issue.evidence_ids:
        return _with_confidence(issue, min(issue.confidence, 0.45))
    return _with_confidence(issue, min(issue.confidence, 0.55))


def _looks_like_style_nit(issue: ReviewIssue) -> bool:
    message = issue.message.lower()
    return "style" in message or "naming convention" in message


def _issue_id(issue: ReviewIssue) -> str:
    line = issue.line if issue.line is not None else "?"
    return f"{issue.category}:{issue.file}:{line}"


def _render_prompt_export(prompt_name: str, prompt_digest: str) -> str:
    return (
        f"<!-- prompt_hash: {prompt_digest} -->\n\n"
        f"{_load_prompt(prompt_name).rstrip()}\n"
    )


def _load_prompt(prompt_name: str) -> str:
    return (_PROMPT_DIR / prompt_name).read_text(encoding="utf-8")
