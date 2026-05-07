"""Evaluation helpers for deterministic review benchmarks."""

from code_review_agent.eval.cases import EvalCase, load_eval_cases
from code_review_agent.eval.metrics import (
    evaluate_case,
    finding_matches_expected,
    line_range_overlap,
    summarize_case_results,
)
from code_review_agent.eval.runner import (
    PROFILE_THRESHOLDS,
    run_eval_benchmark,
)

__all__ = [
    "EvalCase",
    "PROFILE_THRESHOLDS",
    "evaluate_case",
    "finding_matches_expected",
    "line_range_overlap",
    "load_eval_cases",
    "run_eval_benchmark",
    "summarize_case_results",
]
