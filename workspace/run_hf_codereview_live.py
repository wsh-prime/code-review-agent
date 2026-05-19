from __future__ import annotations

import argparse
import difflib
import json
import os
import shutil
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DATASET = "ronantakizawa/github-codereview"
SPLIT = "test"
TARGET_TOTAL = 24
TARGET_NEGATIVE = 6
POSITIVE_TYPES = {"bug", "security", "performance", "refactor", "suggestion", "question"}
HIGH_SIGNAL_TYPES = {"bug", "security", "performance", "refactor"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--work-dir", default="workspace/hf_codereview_live")
    parser.add_argument("--limit", type=int, default=TARGET_TOTAL)
    parser.add_argument("--negative", type=int, default=TARGET_NEGATIVE)
    parser.add_argument("--max-iter", type=int, default=1)
    parser.add_argument("--context-budget", type=int, default=9000)
    parser.add_argument("--export-prompts", action="store_true")
    parser.add_argument("--reuse-samples", action="store_true")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    work_dir = (project_root / args.work_dir).resolve()
    samples_dir = work_dir / "samples"
    summary_path = work_dir / "summary.json"

    sys.path.insert(0, str(project_root / "src"))
    _import_env_file(project_root / "scripts" / "review-live.env.local")
    _require_live_env()

    from code_review_agent.review.pipeline import run_review_pipeline

    if not args.reuse_samples and work_dir.exists():
        shutil.rmtree(work_dir)
    samples_dir.mkdir(parents=True, exist_ok=True)

    samples = (
        _load_jsonl(work_dir / "samples.jsonl")
        if args.reuse_samples and (work_dir / "samples.jsonl").exists()
        else _download_samples(limit=args.limit, negative_target=args.negative)
    )
    _write_jsonl(work_dir / "samples.jsonl", samples)

    results: list[dict[str, Any]] = []
    for index, sample in enumerate(samples):
        sample_id = f"sample_{index:03d}"
        sample_dir = samples_dir / sample_id
        repo_dir = sample_dir / "repo"
        out_dir = sample_dir / "review"
        patch_path = sample_dir / "changes.patch"
        _prepare_sample(sample, repo_dir=repo_dir, patch_path=patch_path)

        started = time.monotonic()
        result: dict[str, Any] = {
            "sample_id": sample_id,
            "repo_name": sample.get("repo_name"),
            "file_path": sample.get("file_path"),
            "comment_type": sample.get("comment_type"),
            "is_negative": sample.get("is_negative"),
            "quality_score": sample.get("quality_score"),
            "reviewer_comment": sample.get("reviewer_comment"),
            "status": "ok",
        }
        print(f"[{index + 1}/{len(samples)}] {sample_id} {sample.get('comment_type')} {sample.get('file_path')}")
        try:
            report = run_review_pipeline(
                repo_dir,
                patch_path,
                out_dir,
                mode="hybrid-live",
                export_prompts=args.export_prompts,
                max_iter=args.max_iter,
                context_budget=args.context_budget,
                max_files_per_agent_call=2,
                max_evidence_per_file=40,
                max_context_refill_rounds=1,
                max_context_requests=4,
            )
            summary = report.get("summary", {})
            result.update(
                {
                    "mode": summary.get("mode"),
                    "fallback_used": summary.get("fallback_used"),
                    "finding_count": summary.get("finding_count", 0),
                    "needs_human_review_count": summary.get(
                        "needs_human_review_count", 0
                    ),
                    "discarded_count": summary.get("discarded_count", 0),
                    "agent_run_count": summary.get("agent_run_count", 0),
                    "token_in": summary.get("total_token_count_in", 0),
                    "token_out": summary.get("total_token_count_out", 0),
                    "review_shard_count": summary.get("review_shard_count", 0),
                    "context_refill_count": summary.get("context_refill_count", 0),
                    "context_request_count": summary.get("context_request_count", 0),
                    "elapsed_ms": int((time.monotonic() - started) * 1000),
                    "report_path": str(out_dir / "review_report.json"),
                }
            )
            result["emitted_any_issue"] = (
                result["finding_count"] + result["needs_human_review_count"]
            ) > 0
            result["negative_false_positive"] = bool(
                result["is_negative"] and result["emitted_any_issue"]
            )
        except Exception as exc:  # noqa: BLE001 - benchmark should continue.
            result.update(
                {
                    "status": "error",
                    "error_type": exc.__class__.__name__,
                    "error": str(exc),
                    "elapsed_ms": int((time.monotonic() - started) * 1000),
                }
            )
        results.append(result)
        _write_summary(work_dir, results)

    _write_summary(work_dir, results)
    print(f"\nWrote {summary_path}")
    return 0


def _download_samples(*, limit: int, negative_target: int) -> list[dict[str, Any]]:
    positive_target = max(0, limit - negative_target)
    positives: list[dict[str, Any]] = []
    negatives: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()
    offset = 0
    while (
        (len(positives) < positive_target or len(negatives) < negative_target)
        and offset < 5000
    ):
        payload = _fetch_rows(offset=offset, length=100)
        rows = [item["row"] for item in payload.get("rows", [])]
        if not rows:
            break
        for row in rows:
            if not _usable_python_row(row):
                continue
            key = (
                str(row.get("repo_name")),
                int(row.get("pr_number") or -1),
                str(row.get("file_path")),
                str(row.get("comment_type")),
                str(row.get("is_negative")),
            )
            if key in seen:
                continue
            seen.add(key)
            if row.get("is_negative"):
                if len(negatives) < negative_target:
                    negatives.append(row)
                continue
            if row.get("comment_type") not in POSITIVE_TYPES:
                continue
            if row.get("comment_type") in HIGH_SIGNAL_TYPES:
                positives.insert(0, row)
            elif len(positives) < positive_target:
                positives.append(row)
            if len(positives) >= positive_target and len(negatives) >= negative_target:
                break
        offset += 100

    selected = positives[:positive_target] + negatives[:negative_target]
    if len(selected) < limit:
        raise RuntimeError(f"Only selected {len(selected)} usable samples, wanted {limit}.")
    return selected


def _fetch_rows(*, offset: int, length: int) -> dict[str, Any]:
    query = urllib.parse.urlencode(
        {
            "dataset": DATASET,
            "config": "default",
            "split": SPLIT,
            "offset": str(offset),
            "length": str(length),
        }
    )
    url = f"https://datasets-server.huggingface.co/rows?{query}"
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


def _usable_python_row(row: dict[str, Any]) -> bool:
    path = str(row.get("file_path") or "")
    before = str(row.get("before_code") or "")
    after = str(row.get("after_code") or "")
    diff_context = str(row.get("diff_context") or "")
    if row.get("language") != "Python" or not path.endswith(".py"):
        return False
    if not before.strip() or not after.strip():
        return False
    if before == after and not diff_context.strip().startswith("@@"):
        return False
    if len(before.splitlines()) > 180 or len(after.splitlines()) > 180:
        return False
    return True


def _prepare_sample(
    sample: dict[str, Any], *, repo_dir: Path, patch_path: Path
) -> None:
    if repo_dir.exists():
        shutil.rmtree(repo_dir)
    repo_dir.mkdir(parents=True, exist_ok=True)
    file_path = str(sample["file_path"]).replace("\\", "/")
    target = repo_dir / file_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(str(sample["after_code"]), encoding="utf-8")
    patch_path.parent.mkdir(parents=True, exist_ok=True)
    before = str(sample["before_code"])
    after = str(sample["after_code"])
    if before == after and str(sample.get("diff_context") or "").strip().startswith("@@"):
        patch_text = _wrap_diff_context(file_path, str(sample["diff_context"]))
    else:
        patch_text = _make_unified_diff(file_path, before, after)
    patch_path.write_text(
        patch_text,
        encoding="utf-8",
    )


def _make_unified_diff(path: str, before: str, after: str) -> str:
    before_lines = before.splitlines()
    after_lines = after.splitlines()
    diff = difflib.unified_diff(
        before_lines,
        after_lines,
        fromfile=f"a/{path}",
        tofile=f"b/{path}",
        n=8,
        lineterm="",
    )
    return "\n".join(diff) + "\n"


def _wrap_diff_context(path: str, diff_context: str) -> str:
    context = diff_context.replace("\r\n", "\n").replace("\r", "\n")
    if not context.endswith("\n"):
        context += "\n"
    return f"--- a/{path}\n+++ b/{path}\n{context}"


def _import_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ[key.strip().lstrip("\ufeff")] = value.strip().strip('"').strip("'")


def _require_live_env() -> None:
    if not (
        os.environ.get("SILICONFLOW_API_KEY")
        or os.environ.get("OPENAI_COMPATIBLE_API_KEY")
    ):
        raise RuntimeError("Missing SILICONFLOW_API_KEY or OPENAI_COMPATIBLE_API_KEY.")


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


def _write_summary(work_dir: Path, results: list[dict[str, Any]]) -> None:
    aggregate = {
        "total": len(results),
        "ok": sum(1 for item in results if item.get("status") == "ok"),
        "errors": sum(1 for item in results if item.get("status") == "error"),
        "fallbacks": sum(1 for item in results if item.get("fallback_used")),
        "negative_cases": sum(1 for item in results if item.get("is_negative")),
        "negative_false_positives": sum(
            1 for item in results if item.get("negative_false_positive")
        ),
        "total_token_in": sum(int(item.get("token_in") or 0) for item in results),
        "total_token_out": sum(int(item.get("token_out") or 0) for item in results),
    }
    payload = {"aggregate": aggregate, "results": results}
    work_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / "summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    lines = [
        "# HF CodeReview Live Benchmark",
        "",
        "## Aggregate",
        "",
        f"- total: {aggregate['total']}",
        f"- ok: {aggregate['ok']}",
        f"- errors: {aggregate['errors']}",
        f"- fallbacks: {aggregate['fallbacks']}",
        f"- negative false positives: {aggregate['negative_false_positives']} / {aggregate['negative_cases']}",
        f"- token in/out: {aggregate['total_token_in']} / {aggregate['total_token_out']}",
        "",
        "## Samples",
        "",
        "| id | type | negative | status | findings | nhr | fallback | tokens | file |",
        "|---|---|---:|---|---:|---:|---:|---:|---|",
    ]
    for item in results:
        lines.append(
            "| {sample_id} | {comment_type} | {is_negative} | {status} | {finding_count} | "
            "{needs_human_review_count} | {fallback_used} | {token_in}/{token_out} | {file_path} |".format(
                sample_id=item.get("sample_id", ""),
                comment_type=item.get("comment_type", ""),
                is_negative=str(item.get("is_negative", "")),
                status=item.get("status", ""),
                finding_count=item.get("finding_count", 0),
                needs_human_review_count=item.get("needs_human_review_count", 0),
                fallback_used=str(item.get("fallback_used", "")),
                token_in=item.get("token_in", 0),
                token_out=item.get("token_out", 0),
                file_path=str(item.get("file_path", "")).replace("|", "\\|"),
            )
        )
    (work_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
