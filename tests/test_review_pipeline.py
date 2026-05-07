from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from code_review_agent.context.repo_map import build_repo_map
from code_review_agent.hygiene.classifier import EXPERIMENT
from code_review_agent.models import ReviewIssue
from code_review_agent.review.agents import _AgentTransientError
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
    assert report["summary"]["agent_run_count"] >= 2
    assert report["summary"]["loop_enabled"] is True
    assert report["summary"]["loop_iterations_completed"] >= 1
    assert report["loop"]["enabled"] is True
    assert report["summary"]["discarded_count"] >= 1
    assert any(
        item["filter_reason"] == "invalid_evidence_ids"
        for item in report["discarded"]
    )
    assert "fake:invalid:evidence" in report["missing_evidence_ids"]
    assert report["summary"]["missing_evidence_id_count"] >= 1
    assert report["findings"][0]["category"] == TEST_GAP


def test_report_contains_tracing_summary(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    out = tmp_path / "out"
    patch = tmp_path / "change.patch"
    _write_repo(repo)
    patch.write_text(_test_gap_patch(), encoding="utf-8")

    report = run_review_pipeline(repo, patch, out, mode="hybrid-fake")

    assert report["tracing"]["run_count"] == report["summary"]["agent_run_count"]
    assert report["tracing"]["total_retry_count"] == 0
    assert report["tracing"]["status_counts"]["ok"] >= 1


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

    class FakeLiveAgent:
        model = "test-live-model"

        def review(self, package, *, prior_feedback=None):
            return [
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
            ]

    monkeypatch.setattr(
        pipeline_module.OpenAICompatibleReviewAgent,
        "from_env",
        classmethod(lambda cls: FakeLiveAgent()),
    )

    report = run_review_pipeline(repo, patch, out, mode="hybrid-live")

    assert report["summary"]["mode"] == "hybrid-live"
    assert report["summary"]["context_budget_enabled"] is True
    assert report["summary"]["selected_evidence_count"] >= 1
    assert report["context_budget"]["strategy"] == "risk_first_v1"
    assert report["summary"]["agent_run_count"] == 2
    assert report["summary"]["loop_enabled"] is True
    assert report["agent_runs"][0]["model"] == "test-live-model"
    assert report["findings"][0]["category"] == TEST_GAP
    assert (out / "loop_checkpoint.json").exists()
    assert report["loop"]["checkpoint_path"] == str(out / "loop_checkpoint.json")


def test_review_pipeline_large_live_patch_uses_context_shards(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repo = tmp_path / "repo"
    out = tmp_path / "out"
    patch = tmp_path / "large.patch"
    _write_large_repo(repo, file_count=5)
    patch.write_text(_large_patch(file_count=5), encoding="utf-8")
    calls: list[dict] = []

    def fake_post(url, *, api_key, body, timeout_seconds):
        del url, api_key, timeout_seconds
        calls.append(body)
        content = body["messages"][1]["content"]
        context = json.loads(content.split("ReviewerContext:\n", 1)[1])
        evidence_id = sorted(context["evidence_index"])[0]
        evidence = context["evidence_index"][evidence_id]
        path, _, raw_line = evidence["source"].rpartition(":")
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "issues": [
                                    {
                                        "file": path,
                                        "line": int(raw_line),
                                        "severity": "medium",
                                        "category": TEST_GAP,
                                        "message": "Shard candidate.",
                                        "suggestion": "Update tests.",
                                        "confidence": 0.75,
                                        "evidence_ids": [evidence_id],
                                    }
                                ],
                                "context_requests": [],
                            }
                        )
                    }
                }
            ],
            "usage": {"prompt_tokens": 50, "completion_tokens": 10},
        }

    monkeypatch.setenv("OPENAI_COMPATIBLE_API_KEY", "test-key")
    monkeypatch.setattr(
        pipeline_module,
        "_post_openai_compatible_json",
        fake_post,
        raising=False,
    )
    monkeypatch.setattr(
        "code_review_agent.review.agents._post_openai_compatible_json",
        fake_post,
    )

    report = run_review_pipeline(
        repo,
        patch,
        out,
        mode="hybrid-live",
        max_iter=1,
        context_budget=900,
        max_files_per_agent_call=2,
        max_evidence_per_file=3,
    )

    assert len(calls) == 3
    assert report["summary"]["review_shard_count"] == 3
    assert report["context_budget"]["strategy"] == "file_risk_shards_v1"
    assert report["context_budget"]["shards"]
    assert (out / "live_context_checkpoint.json").exists()


def test_fallback_rules_preserved_on_live_failure(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repo = tmp_path / "repo"
    out = tmp_path / "out"
    patch = tmp_path / "change.patch"
    _write_repo(repo)
    patch.write_text(_test_gap_patch(), encoding="utf-8")

    class FailingLiveAgent:
        model = "test-live-model"

        def review(self, package, *, prior_feedback=None):
            del package, prior_feedback
            raise _AgentTransientError("temporary outage")

    monkeypatch.setattr(
        pipeline_module.OpenAICompatibleReviewAgent,
        "from_env",
        classmethod(lambda cls: FailingLiveAgent()),
    )

    report = run_review_pipeline(repo, patch, out, mode="hybrid-live")

    assert report["summary"]["mode"] == "hybrid-live/fallback-rules"
    assert report["summary"]["fallback_used"] is True
    assert report["summary"]["fallback_reason"] == "temporary outage"
    assert report["findings"][0]["category"] == TEST_GAP
    assert report["agent_runs"][0]["status"] == "fallback"
    assert report["agent_runs"][0]["fallback_used"] is True
    assert report["loop"]["iterations_completed"] == 0


def test_review_pipeline_hybrid_fake_accepts_max_iter(
    tmp_path: Path,
) -> None:
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
        max_iter=1,
    )

    assert report["loop"]["max_iter"] == 1
    assert report["summary"]["loop_iterations_completed"] == 1


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


def _write_large_repo(root: Path, *, file_count: int) -> None:
    (root / "src" / "shop").mkdir(parents=True)
    (root / "tests").mkdir()
    for index in range(file_count):
        (root / "src" / "shop" / f"service_{index}.py").write_text(
            f"def create_order_{index}(total: int) -> bool:\n"
            "    if total <= 0:\n"
            "        return False\n"
            "    return True\n",
            encoding="utf-8",
        )


def _large_patch(*, file_count: int) -> str:
    parts: list[str] = []
    for index in range(file_count):
        path = f"src/shop/service_{index}.py"
        parts.append(
            f"""diff --git a/{path} b/{path}
--- a/{path}
+++ b/{path}
@@ -1,4 +1,4 @@
 def create_order_{index}(total: int) -> bool:
     if total <= 0:
         return False
-    return True
+    return total > {index}
"""
        )
    return "".join(parts)
