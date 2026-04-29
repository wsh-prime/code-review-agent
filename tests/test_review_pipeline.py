from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from code_review_agent.context.repo_map import build_repo_map
from code_review_agent.hygiene.classifier import EXPERIMENT
from code_review_agent.models import AgentRun, ReviewIssue
from code_review_agent.review.agents import FakeAgentResult
from code_review_agent.review import pipeline as pipeline_module
from code_review_agent.review.pipeline import run_review_pipeline
from code_review_agent.review.risk import DOC_ONLY, EXPERIMENT_ARTIFACT, TEST_GAP


def test_review_pipeline_writes_report_with_findings_and_evidence(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    out = tmp_path / "out"
    patch = tmp_path / "change.patch"
    _write_repo(repo)
    patch.write_text(_test_gap_patch(), encoding="utf-8")

    report = run_review_pipeline(repo, patch, out)

    assert report["summary"]["changed_file_count"] == 1
    assert report["summary"]["finding_count"] == 1
    assert report["findings"][0]["category"] == TEST_GAP
    assert report["changed_files"][0]["new_path"] == "src/shop/service.py"
    assert report["changed_entities"]
    assert any(signal["tag"] == TEST_GAP for signal in report["risk_signals"])
    assert "diff:src/shop/service.py:4" in report["evidence_index"]
    assert (out / "review_report.json").exists()
    assert (out / "review_report.md").exists()


def test_review_pipeline_doc_only_patch_has_no_formal_findings(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    out = tmp_path / "out"
    patch = tmp_path / "docs.patch"
    _write_repo(repo)
    patch.write_text(
        """diff --git a/docs/design.md b/docs/design.md
--- a/docs/design.md
+++ b/docs/design.md
@@ -1 +1,2 @@
 # Design
+More notes.
""",
        encoding="utf-8",
    )

    report = run_review_pipeline(repo, patch, out)

    assert report["findings"] == []
    assert [signal["tag"] for signal in report["risk_signals"]] == [DOC_ONLY]


def test_review_pipeline_loads_repo_map_and_hygiene_files(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    out = tmp_path / "out"
    patch = tmp_path / "artifact.patch"
    repo_map_path = tmp_path / "repo_map.json"
    hygiene_path = tmp_path / "project_hygiene.json"
    _write_repo(repo)
    patch.write_text(
        """diff --git a/src/shop/debug_flow.py b/src/shop/debug_flow.py
new file mode 100644
--- /dev/null
+++ b/src/shop/debug_flow.py
@@ -0,0 +1,2 @@
+def run():
+    return None
""",
        encoding="utf-8",
    )
    repo_map_path.write_text(
        json.dumps(build_repo_map(repo).to_dict(), ensure_ascii=False),
        encoding="utf-8",
    )
    hygiene_path.write_text(
        json.dumps(
            {
                "file_classifications": [
                    {
                        "path": "src/shop/debug_flow.py",
                        "category": EXPERIMENT,
                        "mainline_relevance": "low",
                        "confidence": 0.84,
                        "reason": "Debug helper.",
                        "signals": [],
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    report = run_review_pipeline(
        repo,
        patch,
        out,
        repo_map_path=repo_map_path,
        hygiene_path=hygiene_path,
    )

    assert report["findings"][0]["category"] == EXPERIMENT_ARTIFACT
    assert "hygiene:src/shop/debug_flow.py" in report["evidence_index"]


def test_review_cli_runs_rules_mode_and_writes_reports(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    out = tmp_path / "out"
    patch = tmp_path / "change.patch"
    _write_repo(repo)
    patch.write_text(_test_gap_patch(), encoding="utf-8")
    project_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root / "src")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "code_review_agent.cli",
            "review",
            "--repo",
            str(repo),
            "--diff",
            str(patch),
            "--out",
            str(out),
        ],
        cwd=project_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Code Review Agent Harness - review" in result.stdout
    data = json.loads((out / "review_report.json").read_text(encoding="utf-8"))
    assert data["findings"][0]["category"] == TEST_GAP
    assert (out / "review_report.md").exists()


def test_review_pipeline_hybrid_fake_filters_invalid_agent_evidence(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    out = tmp_path / "out"
    patch = tmp_path / "change.patch"
    _write_repo(repo)
    patch.write_text(_test_gap_patch(), encoding="utf-8")

    report = run_review_pipeline(repo, patch, out, mode="hybrid-fake")

    assert report["summary"]["mode"] == "hybrid-fake"
    assert report["summary"]["agent_run_count"] == 2
    assert report["summary"]["discarded_count"] >= 1
    assert any(
        item["filter_reason"] == "invalid_evidence_ids"
        for item in report["discarded"]
    )
    assert "fake:invalid:evidence" in report["missing_evidence_ids"]
    assert report["summary"]["missing_evidence_id_count"] >= 1
    assert report["findings"][0]["category"] == TEST_GAP


def test_review_pipeline_exports_prompts(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    out = tmp_path / "out"
    patch = tmp_path / "change.patch"
    _write_repo(repo)
    patch.write_text(_test_gap_patch(), encoding="utf-8")

    report = run_review_pipeline(
        repo,
        patch,
        out,
        mode="hybrid-fake",
        export_prompts=True,
    )

    assert report["summary"]["prompt_exported"] is True
    assert report["prompt_exports"]["review_prompt_hash"]
    assert (out / "prompts" / "review_agent_input.json").exists()
    assert (out / "prompts" / "review_agent_prompt.md").exists()


def test_review_pipeline_hybrid_live_uses_openai_compatible_agent(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repo = tmp_path / "repo"
    out = tmp_path / "out"
    patch = tmp_path / "change.patch"
    _write_repo(repo)
    patch.write_text(_test_gap_patch(), encoding="utf-8")

    def fake_live_agent(package):
        return FakeAgentResult(
            findings=[
                ReviewIssue(
                    file="src/shop/service.py",
                    line=4,
                    severity="medium",
                    category=TEST_GAP,
                    message="Live backend candidate.",
                    suggestion="Update tests.",
                    confidence=0.72,
                    evidence_ids=["diff:src/shop/service.py:4"],
                )
            ],
            agent_runs=[
                AgentRun(
                    agent_name="openai_compatible_reviewer",
                    model="test-live-model",
                    prompt_hash="abc",
                    input_evidence_ids=sorted(package.evidence_index),
                    output_issue_ids=["test_gap:src/shop/service.py:4"],
                )
            ],
        )

    monkeypatch.setattr(
        pipeline_module,
        "run_openai_compatible_review_agent",
        fake_live_agent,
    )

    report = run_review_pipeline(repo, patch, out, mode="hybrid-live")

    assert report["summary"]["mode"] == "hybrid-live"
    assert report["summary"]["agent_run_count"] == 1
    assert report["agent_runs"][0]["model"] == "test-live-model"
    assert report["findings"][0]["category"] == TEST_GAP


def _write_repo(root: Path) -> None:
    (root / "src" / "shop").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "docs").mkdir()
    (root / "src" / "shop" / "service.py").write_text(
        "def create_order(total: int) -> bool:\n"
        "    if total <= 0:\n"
        "        return False\n"
        "    return total > 10\n",
        encoding="utf-8",
    )
    (root / "tests" / "test_service.py").write_text(
        "from shop.service import create_order\n\n"
        "def test_create_order():\n"
        "    assert create_order(20)\n",
        encoding="utf-8",
    )
    (root / "docs" / "design.md").write_text("# Design\nMore notes.\n", encoding="utf-8")


def _test_gap_patch() -> str:
    return """diff --git a/src/shop/service.py b/src/shop/service.py
--- a/src/shop/service.py
+++ b/src/shop/service.py
@@ -1,4 +1,4 @@
 def create_order(total: int) -> bool:
     if total <= 0:
         return False
-    return True
+    return total > 10
"""
