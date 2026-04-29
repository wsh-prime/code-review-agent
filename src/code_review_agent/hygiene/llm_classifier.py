"""LLM-based semantic classifier for hygiene analysis.

Provides:
- ``LLMClassifier`` – a structural Protocol that any real LLM backend must
  satisfy.
- ``FakeLLMClassifier`` – a deterministic, API-free implementation for unit
  tests and CI.
- ``classify_with_llm()`` – orchestrates classification + schema validation
  for a list of evidence objects.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from code_review_agent.hygiene.taxonomy import (
    ALL_TYPES,
    DESCRIPTIONS,
    SUGGESTED_ACTIONS,
    UNCERTAIN,
)
from code_review_agent.models import HygieneEvidence, SemanticClassification


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class LLMClassifier(Protocol):
    """Interface that every LLM backend must implement.

    Implementations must:
    - Choose ``artifact_type`` exclusively from
      :data:`~code_review_agent.hygiene.taxonomy.ALL_TYPES`.
    - Return ``confidence`` in ``[0.0, 1.0]``.
    - Populate ``reason`` with a non-empty string.
    - Fall back to ``uncertain`` when evidence is ambiguous.
    """

    def classify(
        self,
        evidence: HygieneEvidence,
        taxonomy_descriptions: dict[str, str],
    ) -> SemanticClassification: ...


# ---------------------------------------------------------------------------
# Fake implementation (deterministic, no API calls)
# ---------------------------------------------------------------------------


class FakeLLMClassifier:
    """Deterministic fake classifier for unit tests and dry runs.

    Parameters
    ----------
    responses:
        Optional mapping of ``file_path → artifact_type``.  Any path not in
        the mapping is classified as ``uncertain``.
    default_confidence:
        Confidence assigned to resolved types (not applied to ``uncertain``).
    """

    def __init__(
        self,
        responses: dict[str, str] | None = None,
        *,
        default_confidence: float = 0.85,
    ) -> None:
        self._responses: dict[str, str] = responses or {}
        self._default_confidence = default_confidence

    def classify(
        self,
        evidence: HygieneEvidence,
        taxonomy_descriptions: dict[str, str],
    ) -> SemanticClassification:
        artifact_type = self._responses.get(evidence.path, UNCERTAIN)
        if artifact_type not in ALL_TYPES:
            artifact_type = UNCERTAIN

        confidence = (
            self._default_confidence if artifact_type != UNCERTAIN else 0.35
        )

        return SemanticClassification(
            path=evidence.path,
            artifact_type=artifact_type,
            confidence=confidence,
            suggested_action=SUGGESTED_ACTIONS[artifact_type],
            reason=f"FakeLLM: classified as {artifact_type}",
            evidence=evidence.signals[:3],
        )


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def classify_with_llm(
    evidence_list: list[HygieneEvidence],
    classifier: LLMClassifier,
) -> list[SemanticClassification]:
    """Classify each evidence item and validate the LLM output schema.

    Raises
    ------
    ValueError
        If the classifier returns an invalid ``artifact_type``, an
        out-of-range ``confidence``, or an empty ``reason``.
    """
    results: list[SemanticClassification] = []
    for evidence in evidence_list:
        result = classifier.classify(evidence, DESCRIPTIONS)
        validate_semantic_classification(result)
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------


def validate_semantic_classification(cls: SemanticClassification) -> None:
    """Raise :exc:`ValueError` if *cls* violates the output contract."""
    if cls.artifact_type not in ALL_TYPES:
        raise ValueError(
            f"Invalid artifact_type '{cls.artifact_type}'. "
            f"Must be one of: {sorted(ALL_TYPES)}"
        )
    if not (0.0 <= cls.confidence <= 1.0):
        raise ValueError(
            f"confidence must be in [0.0, 1.0], got {cls.confidence}"
        )
    if not cls.reason or not cls.reason.strip():
        raise ValueError("SemanticClassification.reason must not be empty.")
    expected_action = SUGGESTED_ACTIONS.get(cls.artifact_type)
    if expected_action and cls.suggested_action != expected_action:
        raise ValueError(
            f"suggested_action '{cls.suggested_action}' does not match "
            f"expected '{expected_action}' for artifact_type '{cls.artifact_type}'."
        )
