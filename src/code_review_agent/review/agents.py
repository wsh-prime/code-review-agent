"""Fake review agents used to exercise the evidence-first harness."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol
from urllib import error, request

from code_review_agent.models import AgentRun, EvidencePackage, ReviewIssue, RiskSignal
from code_review_agent.review.risk import DOC_ONLY, risk_evidence_id


RECALL_BIASED_REVIEWER = "recall_biased_reviewer"
PRECISION_BIASED_CRITIC = "precision_biased_critic"
SAME_STRATEGY = "same_strategy"
CROSS_STRATEGY = "cross_strategy"
FAKE_MODEL_NAME = "fake-llm"
DEFAULT_OPENAI_COMPATIBLE_BASE_URL = "https://api.siliconflow.cn/v1"
DEFAULT_OPENAI_COMPATIBLE_MODEL = "deepseek-ai/DeepSeek-V4-Flash"
OPENAI_COMPATIBLE_TIMEOUT_SECONDS = 60

_PROMPT_DIR = Path(__file__).with_name("prompts")
_REVIEW_PROMPT = "review_agent.md"
_CRITIC_PROMPT = "critic_agent.md"


class ReviewAgent(Protocol):
    def review(self, package: EvidencePackage) -> list[ReviewIssue]:
        """Return candidate review issues for one evidence package."""


class CriticAgent(Protocol):
    def filter(
        self, issues: list[ReviewIssue], package: EvidencePackage
    ) -> list[ReviewIssue]:
        """Return candidate issues after agent-side criticism."""


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

    def review(self, package: EvidencePackage) -> list[ReviewIssue]:
        if self.strategy == PRECISION_BIASED_CRITIC:
            return [
                issue
                for issue in _issues_from_risk_signals(package)
                if issue.confidence >= 0.75
            ]

        issues = _issues_from_risk_signals(package)
        invalid = _invalid_evidence_probe(package)
        if invalid is not None:
            issues.append(invalid)
        return issues


@dataclass(slots=True)
class FakeLLMCriticAgent:
    """Precision-biased fake critic that downgrades weak candidates."""

    strategy: str = PRECISION_BIASED_CRITIC

    def filter(
        self, issues: list[ReviewIssue], package: EvidencePackage
    ) -> list[ReviewIssue]:
        if self.strategy == RECALL_BIASED_REVIEWER:
            return list(issues)

        reviewed: list[ReviewIssue] = []
        for issue in issues:
            if _looks_like_style_nit(issue):
                continue
            if not any(eid in package.evidence_index for eid in issue.evidence_ids):
                reviewed.append(_with_confidence(issue, min(issue.confidence, 0.45)))
                continue
            if issue.category in {"api_change", "behavior_change", "security_sensitive"}:
                reviewed.append(_with_confidence(issue, min(issue.confidence, 0.55)))
                continue
            reviewed.append(issue)
        return reviewed


@dataclass(slots=True)
class OpenAICompatibleReviewAgent:
    """OpenAI-compatible chat-completions reviewer using only stdlib HTTP."""

    api_key: str
    base_url: str = DEFAULT_OPENAI_COMPATIBLE_BASE_URL
    model: str = DEFAULT_OPENAI_COMPATIBLE_MODEL
    timeout_seconds: int = OPENAI_COMPATIBLE_TIMEOUT_SECONDS

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

    def review(self, package: EvidencePackage) -> list[ReviewIssue]:
        body = {
            "model": self.model,
            "temperature": 0,
            "max_tokens": 1200,
            "messages": [
                {
                    "role": "system",
                    "content": _load_prompt(_REVIEW_PROMPT),
                },
                {
                    "role": "user",
                    "content": (
                        "Return only a JSON array of ReviewIssue objects. "
                        "Use only evidence_ids present in evidence_index.\n\n"
                        f"EvidencePackage:\n{json.dumps(package.to_dict(), ensure_ascii=False)}"
                    ),
                },
            ],
        }
        response = _post_openai_compatible_json(
            f"{self.base_url.rstrip('/')}/chat/completions",
            api_key=self.api_key,
            body=body,
            timeout_seconds=self.timeout_seconds,
        )
        content = _chat_completion_text(response)
        return _issues_from_llm_json(content)


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
    return FakeAgentResult(
        findings=issues,
        agent_runs=[
            AgentRun(
                agent_name="openai_compatible_reviewer",
                model=reviewer.model,
                prompt_hash=prompt_hash(_REVIEW_PROMPT),
                input_evidence_ids=sorted(package.evidence_index),
                output_issue_ids=[_issue_id(issue) for issue in issues],
                fallback_used=False,
            )
        ],
    )


def export_agent_prompts(
    package: EvidencePackage,
    out_dir: Path | str,
    *,
    mode: str,
    pair_strategy: str = CROSS_STRATEGY,
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
    review_input_path.write_text(
        json.dumps(
            {
                "mode": mode,
                "pair_strategy": pair_strategy,
                "prompt_hash": review_hash,
                "package": package.to_dict(),
                "redacted_metadata_fields": package.metadata.get("redacted", []),
            },
            indent=2,
            ensure_ascii=False,
        ),
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
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"OpenAI-compatible API returned HTTP {exc.code}: {_truncate(raw)}"
        ) from exc
    except error.URLError as exc:
        raise RuntimeError(f"OpenAI-compatible API request failed: {exc.reason}") from exc
    return json.loads(raw)


def _chat_completion_text(response: dict) -> str:
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("OpenAI-compatible response missing choices[0].message.content") from exc


def _issues_from_llm_json(content: str) -> list[ReviewIssue]:
    parsed = json.loads(_extract_json_array(content))
    if not isinstance(parsed, list):
        raise ValueError("LLM review output must be a JSON array.")
    return [_issue_from_dict(item) for item in parsed]


def _extract_json_array(content: str) -> str:
    stripped = content.strip()
    if stripped.startswith("```"):
        stripped = stripped.removeprefix("```json").removeprefix("```").strip()
        stripped = stripped.removesuffix("```").strip()
    if stripped.startswith("["):
        return stripped
    start = stripped.find("[")
    end = stripped.rfind("]")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("LLM review output did not contain a JSON array.")
    return stripped[start : end + 1]


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
        if len(parts) >= 3 and parts[0] == "diff":
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
