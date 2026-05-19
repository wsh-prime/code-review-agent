from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any


DATA_URL = (
    "https://huggingface.co/datasets/Qodo/PR-Review-Bench/resolve/main/"
    "git_code_review_bench_100_w_open_prs.jsonl"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--work-dir", default="workspace/qodo_pr_review_bench_live")
    parser.add_argument("--dataset-jsonl", default="workspace/qodo_pr_review_bench/git_code_review_bench_100_w_open_prs.jsonl")
    parser.add_argument("--rules-jsonl", default="workspace/qodo_pr_review_bench/rules_for_repo.jsonl")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--max-iter", type=int, default=1)
    parser.add_argument("--context-budget", type=int, default=9000)
    parser.add_argument("--export-prompts", action="store_true")
    parser.add_argument("--reuse-diffs", action="store_true")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    work_dir = (project_root / args.work_dir).resolve()
    dataset_path = (project_root / args.dataset_jsonl).resolve()
    rules_path = (project_root / args.rules_jsonl).resolve()

    sys.path.insert(0, str(project_root / "src"))
    _import_env_file(project_root / "scripts" / "review-live.env.local")
    _require_live_env()

    from code_review_agent.review.pipeline import run_review_pipeline

    if not args.reuse_diffs and work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    if not dataset_path.exists():
        dataset_path.parent.mkdir(parents=True, exist_ok=True)
        _download(DATA_URL, dataset_path)
    rules_by_repo = _load_rules_by_repo(rules_path)

    rows = _load_jsonl(dataset_path)
    selected = rows[args.start : args.start + args.limit]
    (work_dir / "selected_samples.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in selected) + "\n",
        encoding="utf-8",
    )

    results: list[dict[str, Any]] = []
    for index, row in enumerate(selected):
        global_index = args.start + index
        sample_id = f"qodo_{global_index:03d}"
        sample_dir = work_dir / "samples" / sample_id
        repo_dir = sample_dir / "repo"
        out_dir = sample_dir / "review"
        patch_path = sample_dir / "changes.patch"
        repo_dir.mkdir(parents=True, exist_ok=True)
        patch_path.parent.mkdir(parents=True, exist_ok=True)

        result: dict[str, Any] = {
            "sample_id": sample_id,
            "dataset_index": global_index,
            "repo": row.get("repo"),
            "pr_url_to_review": row.get("pr_url_to_review"),
            "ground_truth_issue_count": int(row.get("num_of_issues") or len(row.get("issues", []))),
            "status": "ok",
        }
        print(
            f"[{index + 1}/{len(selected)}] {sample_id} "
            f"{row.get('repo')} issues={result['ground_truth_issue_count']}"
        )
        started = time.monotonic()
        try:
            if not args.reuse_diffs or not patch_path.exists():
                _download_pr_diff(str(row["pr_url_to_review"]), patch_path)
            result["diff_bytes"] = patch_path.stat().st_size
            report = run_review_pipeline(
                repo_dir,
                patch_path,
                out_dir,
                mode="hybrid-live",
                review_guidelines=rules_by_repo.get(str(row.get("repo")), []),
                export_prompts=args.export_prompts,
                max_iter=args.max_iter,
                context_budget=args.context_budget,
                max_files_per_agent_call=4,
                max_evidence_per_file=80,
                max_context_refill_rounds=1,
                max_context_requests=8,
            )
            eval_result = _evaluate_report(row, report)
            summary = report.get("summary", {})
            result.update(
                {
                    "mode": summary.get("mode"),
                    "fallback_used": summary.get("fallback_used"),
                    "finding_count": summary.get("finding_count", 0),
                    "needs_human_review_count": summary.get("needs_human_review_count", 0),
                    "discarded_count": summary.get("discarded_count", 0),
                    "agent_run_count": summary.get("agent_run_count", 0),
                    "token_in": summary.get("total_token_count_in", 0),
                    "token_out": summary.get("total_token_count_out", 0),
                    "review_shard_count": summary.get("review_shard_count", 0),
                    "context_refill_count": summary.get("context_refill_count", 0),
                    "context_request_count": summary.get("context_request_count", 0),
                    "elapsed_ms": int((time.monotonic() - started) * 1000),
                    "report_path": str(out_dir / "review_report.json"),
                    **eval_result,
                }
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
        _write_outputs(work_dir, results)

    _write_outputs(work_dir, results)
    print(f"\nWrote {work_dir / 'summary.md'}")
    print(f"Wrote {work_dir / 'summary.json'}")
    return 0


def _evaluate_report(row: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    gt_issues = list(row.get("issues", []))
    findings = list(report.get("findings", []))
    nhr = list(report.get("needs_human_review", []))
    official = findings
    broad = [*findings, *nhr]
    strict_matches = _match_issues(gt_issues, official, tolerance=0)
    broad_strict_matches = _match_issues(gt_issues, broad, tolerance=0)
    line10_matches = _match_issues(gt_issues, official, tolerance=10)
    broad_line10_matches = _match_issues(gt_issues, broad, tolerance=10)
    file_matches = _match_issues(gt_issues, official, file_only=True)
    broad_file_matches = _match_issues(gt_issues, broad, file_only=True)

    return {
        "gt_matched_findings_exact": len(strict_matches["matched_gt"]),
        "gt_matched_broad_exact": len(broad_strict_matches["matched_gt"]),
        "gt_matched_findings_line10": len(line10_matches["matched_gt"]),
        "gt_matched_broad_line10": len(broad_line10_matches["matched_gt"]),
        "gt_matched_findings_file": len(file_matches["matched_gt"]),
        "gt_matched_broad_file": len(broad_file_matches["matched_gt"]),
        "unmatched_findings_line10": line10_matches["unmatched_pred_count"],
        "unmatched_broad_line10": broad_line10_matches["unmatched_pred_count"],
    }


def _match_issues(
    gt_issues: list[dict[str, Any]],
    predictions: list[dict[str, Any]],
    *,
    tolerance: int = 0,
    file_only: bool = False,
) -> dict[str, Any]:
    matched_gt: set[int] = set()
    matched_pred: set[int] = set()
    for pred_index, pred in enumerate(predictions):
        pred_file = _norm_path(str(pred.get("file") or ""))
        pred_line = pred.get("line")
        if not isinstance(pred_line, int):
            pred_line = None
        for gt_index, gt in enumerate(gt_issues):
            if gt_index in matched_gt:
                continue
            if pred_file != _norm_path(str(gt.get("file_path") or "")):
                continue
            if file_only:
                matched_gt.add(gt_index)
                matched_pred.add(pred_index)
                break
            if pred_line is None:
                continue
            start = int(gt.get("start_line") or gt.get("end_line") or 0)
            end = int(gt.get("end_line") or gt.get("start_line") or start)
            if start > end:
                start, end = end, start
            if start - tolerance <= pred_line <= end + tolerance:
                matched_gt.add(gt_index)
                matched_pred.add(pred_index)
                break
    return {
        "matched_gt": matched_gt,
        "matched_pred": matched_pred,
        "unmatched_pred_count": max(0, len(predictions) - len(matched_pred)),
    }


def _write_outputs(work_dir: Path, results: list[dict[str, Any]]) -> None:
    ok = [item for item in results if item.get("status") == "ok"]
    gt_total = sum(int(item.get("ground_truth_issue_count") or 0) for item in ok)
    finding_total = sum(int(item.get("finding_count") or 0) for item in ok)
    broad_total = finding_total + sum(int(item.get("needs_human_review_count") or 0) for item in ok)
    aggregate = {
        "total": len(results),
        "ok": len(ok),
        "errors": sum(1 for item in results if item.get("status") == "error"),
        "fallbacks": sum(1 for item in ok if item.get("fallback_used")),
        "ground_truth_issues": gt_total,
        "findings": finding_total,
        "findings_plus_nhr": broad_total,
        "finding_recall_exact": _rate(sum(int(item.get("gt_matched_findings_exact") or 0) for item in ok), gt_total),
        "broad_recall_exact": _rate(sum(int(item.get("gt_matched_broad_exact") or 0) for item in ok), gt_total),
        "finding_recall_line10": _rate(sum(int(item.get("gt_matched_findings_line10") or 0) for item in ok), gt_total),
        "broad_recall_line10": _rate(sum(int(item.get("gt_matched_broad_line10") or 0) for item in ok), gt_total),
        "finding_recall_file": _rate(sum(int(item.get("gt_matched_findings_file") or 0) for item in ok), gt_total),
        "broad_recall_file": _rate(sum(int(item.get("gt_matched_broad_file") or 0) for item in ok), gt_total),
        "finding_precision_line10": _rate(
            finding_total - sum(int(item.get("unmatched_findings_line10") or 0) for item in ok),
            finding_total,
        ),
        "broad_precision_line10": _rate(
            broad_total - sum(int(item.get("unmatched_broad_line10") or 0) for item in ok),
            broad_total,
        ),
        "total_token_in": sum(int(item.get("token_in") or 0) for item in ok),
        "total_token_out": sum(int(item.get("token_out") or 0) for item in ok),
    }
    payload = {"aggregate": aggregate, "results": results}
    (work_dir / "summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    lines = [
        "# Qodo PR-Review-Bench Live Summary",
        "",
        "## Aggregate",
        "",
    ]
    for key, value in aggregate.items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Samples",
            "",
            "| id | repo | gt | F | NHR | recall F@10 | recall broad@10 | precision F@10 | fallback | tokens |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for item in results:
        gt = int(item.get("ground_truth_issue_count") or 0)
        f = int(item.get("finding_count") or 0)
        broad = f + int(item.get("needs_human_review_count") or 0)
        lines.append(
            "| {sample_id} | {repo} | {gt} | {f} | {nhr} | {rf} | {rb} | {pf} | {fallback} | {tokens} |".format(
                sample_id=item.get("sample_id"),
                repo=str(item.get("repo", "")).replace("|", "\\|"),
                gt=gt,
                f=f,
                nhr=item.get("needs_human_review_count", 0),
                rf=_rate(int(item.get("gt_matched_findings_line10") or 0), gt),
                rb=_rate(int(item.get("gt_matched_broad_line10") or 0), gt),
                pf=_rate(f - int(item.get("unmatched_findings_line10") or 0), f),
                fallback=item.get("fallback_used", ""),
                tokens=f"{item.get('token_in', 0)}/{item.get('token_out', 0)}",
            )
        )
    lines.extend(
        [
            "",
            "## Metric Notes",
            "",
            "- Exact recall requires same file and predicted line inside the ground-truth issue range.",
            "- Line10 recall allows the predicted line to be within +/-10 lines of the ground-truth range.",
            "- Broad metrics count both findings and needs_human_review as detections.",
            "- Precision here is location-based and deterministic; it does not judge semantic equivalence.",
        ]
    )
    (work_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _download_pr_diff(pr_url: str, path: Path) -> None:
    _download(f"{pr_url.rstrip('/')}.diff", path)


def _download(url: str, path: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "code-review-agent-benchmark"})
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                data = response.read()
            break
        except Exception as exc:  # noqa: BLE001 - benchmark downloads should retry.
            last_error = exc
            if attempt >= 3:
                raise
            time.sleep(float(attempt * 2))
    else:  # pragma: no cover - loop always breaks or raises.
        raise RuntimeError(f"Download failed: {url}") from last_error
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _load_rules_by_repo(path: Path) -> dict[str, list[dict[str, Any]]]:
    if not path.exists():
        return {}
    rules: dict[str, list[dict[str, Any]]] = {}
    for row in _load_jsonl(path):
        repo = str(row.get("repo") or "")
        extracted_rules = row.get("extracted_rules", [])
        if repo and isinstance(extracted_rules, list):
            rules[repo] = [
                item for item in extracted_rules if isinstance(item, dict)
            ]
    return rules


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


def _rate(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return round(numerator / denominator, 4)


def _norm_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


if __name__ == "__main__":
    raise SystemExit(main())
