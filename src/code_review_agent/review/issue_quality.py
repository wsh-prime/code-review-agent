"""Shared heuristics for low-signal review issue control."""

from __future__ import annotations

from code_review_agent.models import ReviewIssue


STYLE_KEYWORDS: frozenset[str] = frozenset(
    {
        "blank line",
        "code style",
        "format",
        "import order",
        "indentation",
        "line length",
        "naming convention",
        "pep 8",
        "pep8",
        "style preference",
        "trailing space",
        "variable name",
        "whitespace",
    }
)
LOW_VALUE_CATEGORIES = frozenset({"maintainability", "test_quality"})
LOW_VALUE_REVIEW_KEYWORDS = frozenset(
    {
        "add a comment",
        "add a docstring",
        "add assertions",
        "comment clarifying",
        "consider adding",
        "could be stronger",
        "document that",
        "does not assert",
        "not explicitly documented",
    }
)
SPECULATIVE_KEYWORDS = frozenset({"could ", "may ", "might ", "potentially "})
CONCRETE_FAILURE_KEYWORDS = frozenset(
    {
        "breaks",
        "crashes",
        "data loss",
        "drops",
        "duplicates",
        "fails",
        "failure",
        "incorrect",
        "leaks",
        "raises",
        "regression",
        "security",
        "skips",
        "timeout",
        "unbounded",
        "wrong",
    }
)


def is_style_preference(issue: ReviewIssue) -> bool:
    """Return True for style-only issues that should not become findings."""

    lower = issue.message.lower()
    return any(keyword in lower for keyword in STYLE_KEYWORDS)


def is_low_signal_review_suggestion(issue: ReviewIssue) -> bool:
    """Return True for non-actionable review suggestions.

    This intentionally keeps concrete correctness/security failures. It only
    removes review noise such as comment requests and speculative claims without
    a failure mode.
    """

    text = f"{issue.message} {issue.suggestion}".lower()
    if issue.category in LOW_VALUE_CATEGORIES and any(
        keyword in text for keyword in LOW_VALUE_REVIEW_KEYWORDS
    ):
        return True
    if issue.category == "correctness" and any(
        keyword in text for keyword in SPECULATIVE_KEYWORDS
    ):
        return not any(keyword in text for keyword in CONCRETE_FAILURE_KEYWORDS)
    return False
