"""Load planted-bug eval cases for deterministic review benchmarks."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class EvalCase:
    """One benchmark case with a patch and deterministic ground truth."""

    case_id: str
    patch: str
    patch_path: Path
    ground_truth_path: Path
    ground_truth: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["patch_path"] = str(self.patch_path)
        data["ground_truth_path"] = str(self.ground_truth_path)
        return data


def load_eval_cases(cases_root: Path | str) -> list[EvalCase]:
    """Load eval cases from ``ground_truth/*.json`` under a cases root."""

    root = Path(cases_root)
    ground_truth_dir = root / "ground_truth"
    if not ground_truth_dir.exists():
        raise FileNotFoundError(f"Missing eval ground_truth directory: {ground_truth_dir}")

    cases: list[EvalCase] = []
    for ground_truth_path in sorted(ground_truth_dir.glob("*.json")):
        data = json.loads(ground_truth_path.read_text(encoding="utf-8"))
        case_id = str(data.get("case_id", ground_truth_path.stem))
        patch = str(data.get("patch", ""))
        if not patch:
            raise ValueError(f"Eval case {case_id} is missing a patch path.")
        patch_path = root / patch
        if not patch_path.exists():
            raise FileNotFoundError(f"Eval case {case_id} patch not found: {patch_path}")

        cases.append(
            EvalCase(
                case_id=case_id,
                patch=patch,
                patch_path=patch_path,
                ground_truth_path=ground_truth_path,
                ground_truth=data,
            )
        )

    if not cases:
        raise ValueError(f"No eval ground truth files found under: {ground_truth_dir}")
    return cases

