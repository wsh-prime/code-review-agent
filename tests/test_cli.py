from __future__ import annotations

import subprocess
import sys
import os
from pathlib import Path


def test_cli_help_returns_success() -> None:
    project_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root / "src")
    result = subprocess.run(
        [sys.executable, "-m", "code_review_agent.cli", "--help"],
        cwd=project_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "code-review-agent" in result.stdout
    assert "hygiene" in result.stdout
    assert "map" in result.stdout
    assert "review" in result.stdout
    assert "eval" in result.stdout


def test_hygiene_help_includes_classifier_options() -> None:
    project_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root / "src")
    result = subprocess.run(
        [sys.executable, "-m", "code_review_agent.cli", "hygiene", "--help"],
        cwd=project_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "--classifier" in result.stdout
    assert "--summary" in result.stdout
    assert "rules" in result.stdout
    assert "hybrid" in result.stdout


def test_review_help_includes_pipeline_options() -> None:
    project_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root / "src")
    result = subprocess.run(
        [sys.executable, "-m", "code_review_agent.cli", "review", "--help"],
        cwd=project_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "--diff" in result.stdout
    assert "--repo-map" in result.stdout
    assert "--hygiene" in result.stdout
    assert "--mode" in result.stdout
    assert "--max-iter" in result.stdout
    assert "--resume" in result.stdout
    assert "--context-budget" in result.stdout
    assert "--max-files-per-agent-call" in result.stdout
    assert "hybrid-live" in result.stdout


def test_eval_help_includes_benchmark_options() -> None:
    project_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root / "src")
    result = subprocess.run(
        [sys.executable, "-m", "code_review_agent.cli", "eval", "--help"],
        cwd=project_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "--cases" in result.stdout
    assert "--out" in result.stdout
    assert "--mode" in result.stdout
    assert "hybrid-fake" in result.stdout
