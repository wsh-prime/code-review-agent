from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", default="workspace/hf_codereview_live")
    args = parser.parse_args()

    work_dir = Path(args.work_dir)
    samples = _load_jsonl(work_dir / "samples.jsonl")
    summary = json.loads((work_dir / "summary.json").read_text(encoding="utf-8"))
    results_by_id = {item["sample_id"]: item for item in summary["results"]}

    rows: list[dict[str, Any]] = []
    for index, sample in enumerate(samples):
        sample_id = f"sample_{index:03d}"
        result = results_by_id.get(sample_id, {"status": "missing"})
        report_path = work_dir / "samples" / sample_id / "review" / "review_report.json"
        report = (
            json.loads(report_path.read_text(encoding="utf-8"))
            if report_path.exists()
            else {}
        )
        findings = report.get("findings", [])
        nhr = report.get("needs_human_review", [])
        discarded = report.get("discarded", [])
        all_issues = [*findings, *nhr]
        rows.append(
            {
                "sample_id": sample_id,
                "sample": sample,
                "result": result,
                "report": report,
                "findings": findings,
                "needs_human_review": nhr,
                "discarded": discarded,
                "all_issues": all_issues,
                "emitted_any_issue": bool(all_issues),
                "emitted_finding": bool(findings),
            }
        )

    metrics = _compute_metrics(rows)
    _write_outputs(work_dir, metrics, rows)
    print(json.dumps(metrics["headline"], ensure_ascii=False, indent=2))
    print(f"Wrote {work_dir / 'metrics.json'}")
    print(f"Wrote {work_dir / 'metrics.md'}")
    return 0


def _compute_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    ok_rows = [row for row in rows if row["result"].get("status") == "ok"]
    positive_rows = [row for row in ok_rows if not row["sample"].get("is_negative")]
    negative_rows = [row for row in ok_rows if row["sample"].get("is_negative")]
    high_signal_rows = [
        row
        for row in positive_rows
        if row["sample"].get("comment_type") in {"bug", "security", "performance", "refactor"}
    ]

    latencies = [int(row["result"].get("elapsed_ms") or 0) for row in ok_rows]
    token_in = [int(row["result"].get("token_in") or 0) for row in ok_rows]
    token_out = [int(row["result"].get("token_out") or 0) for row in ok_rows]
    findings_counts = [len(row["findings"]) for row in ok_rows]
    nhr_counts = [len(row["needs_human_review"]) for row in ok_rows]
    discarded_counts = [len(row["discarded"]) for row in ok_rows]

    issue_categories = Counter()
    nhr_categories = Counter()
    risk_tags = Counter()
    discard_reasons = Counter()
    by_type: dict[str, dict[str, Any]] = {}
    for row in ok_rows:
        comment_type = str(row["sample"].get("comment_type"))
        bucket = by_type.setdefault(
            comment_type,
            {
                "total": 0,
                "any_issue": 0,
                "finding": 0,
                "needs_human_review": 0,
                "line_within_3": 0,
                "line_within_10": 0,
            },
        )
        bucket["total"] += 1
        bucket["any_issue"] += int(row["emitted_any_issue"])
        bucket["finding"] += int(row["emitted_finding"])
        bucket["needs_human_review"] += int(bool(row["needs_human_review"]))
        line_match = _line_match(row)
        bucket["line_within_3"] += int(line_match["within_3"])
        bucket["line_within_10"] += int(line_match["within_10"])

        for issue in row["findings"]:
            issue_categories[str(issue.get("category"))] += 1
        for issue in row["needs_human_review"]:
            nhr_categories[str(issue.get("category"))] += 1
        for risk in row["report"].get("risk_signals", []):
            risk_tags[str(risk.get("tag"))] += 1
        for item in row["discarded"]:
            discard_reasons[str(item.get("filter_reason", "loop_or_unknown"))] += 1

    positive_any = _rate(sum(row["emitted_any_issue"] for row in positive_rows), len(positive_rows))
    positive_finding = _rate(sum(row["emitted_finding"] for row in positive_rows), len(positive_rows))
    negative_silence = _rate(
        sum(not row["emitted_any_issue"] for row in negative_rows), len(negative_rows)
    )
    negative_strict_silence = _rate(
        sum(not row["emitted_finding"] for row in negative_rows), len(negative_rows)
    )
    high_signal_any = _rate(
        sum(row["emitted_any_issue"] for row in high_signal_rows), len(high_signal_rows)
    )
    line_matches = [_line_match(row) for row in positive_rows if row["emitted_any_issue"]]

    headline = {
        "total": total,
        "ok": len(ok_rows),
        "success_rate": _rate(len(ok_rows), total),
        "fallback_rate": _rate(
            sum(bool(row["result"].get("fallback_used")) for row in ok_rows),
            len(ok_rows),
        ),
        "positive_any_issue_rate": positive_any,
        "positive_finding_rate": positive_finding,
        "negative_silence_rate_any_issue": negative_silence,
        "negative_silence_rate_findings_only": negative_strict_silence,
        "high_signal_positive_any_issue_rate": high_signal_any,
        "positive_line_within_3_rate": _rate(
            sum(item["within_3"] for item in line_matches), len(line_matches)
        ),
        "positive_line_within_10_rate": _rate(
            sum(item["within_10"] for item in line_matches), len(line_matches)
        ),
        "avg_token_in": _mean(token_in),
        "avg_token_out": _mean(token_out),
        "p50_latency_ms": _percentile(latencies, 50),
        "p95_latency_ms": _percentile(latencies, 95),
        "avg_findings_per_ok_sample": _mean(findings_counts),
        "avg_needs_human_review_per_ok_sample": _mean(nhr_counts),
        "avg_discarded_per_ok_sample": _mean(discarded_counts),
    }

    return {
        "headline": headline,
        "counts": {
            "positive": len(positive_rows),
            "negative": len(negative_rows),
            "high_signal_positive": len(high_signal_rows),
            "issue_categories": dict(issue_categories),
            "needs_human_review_categories": dict(nhr_categories),
            "risk_tags": dict(risk_tags),
            "discard_reasons": dict(discard_reasons),
        },
        "by_comment_type": {
            key: {
                **value,
                "any_issue_rate": _rate(value["any_issue"], value["total"]),
                "finding_rate": _rate(value["finding"], value["total"]),
                "needs_human_review_rate": _rate(
                    value["needs_human_review"], value["total"]
                ),
                "line_within_3_rate": _rate(value["line_within_3"], value["total"]),
                "line_within_10_rate": _rate(value["line_within_10"], value["total"]),
            }
            for key, value in sorted(by_type.items())
        },
        "sample_rows": [_sample_metric_row(row) for row in rows],
    }


def _line_match(row: dict[str, Any]) -> dict[str, bool]:
    if row["sample"].get("is_negative"):
        return {"within_3": False, "within_10": False}
    comment_line = row["sample"].get("comment_line")
    if not isinstance(comment_line, int) or comment_line <= 0:
        return {"within_3": False, "within_10": False}
    issue_lines = [
        issue.get("line")
        for issue in row["all_issues"]
        if isinstance(issue.get("line"), int)
    ]
    if not issue_lines:
        return {"within_3": False, "within_10": False}
    best_delta = min(abs(line - comment_line) for line in issue_lines)
    return {"within_3": best_delta <= 3, "within_10": best_delta <= 10}


def _sample_metric_row(row: dict[str, Any]) -> dict[str, Any]:
    line_match = _line_match(row)
    return {
        "sample_id": row["sample_id"],
        "comment_type": row["sample"].get("comment_type"),
        "is_negative": row["sample"].get("is_negative"),
        "status": row["result"].get("status"),
        "fallback_used": row["result"].get("fallback_used"),
        "findings": len(row["findings"]),
        "needs_human_review": len(row["needs_human_review"]),
        "discarded": len(row["discarded"]),
        "token_in": row["result"].get("token_in", 0),
        "token_out": row["result"].get("token_out", 0),
        "latency_ms": row["result"].get("elapsed_ms", 0),
        "comment_line": row["sample"].get("comment_line"),
        "line_within_3": line_match["within_3"],
        "line_within_10": line_match["within_10"],
        "file_path": row["sample"].get("file_path"),
    }


def _write_outputs(
    work_dir: Path, metrics: dict[str, Any], rows: list[dict[str, Any]]
) -> None:
    (work_dir / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    lines = [
        "# HF CodeReview Metrics",
        "",
        "## Headline",
        "",
    ]
    for key, value in metrics["headline"].items():
        lines.append(f"- {key}: {_fmt(value, percent=_is_rate_key(key))}")
    lines.extend(["", "## Counts", ""])
    for key, value in metrics["counts"].items():
        lines.append(f"- {key}: `{json.dumps(value, ensure_ascii=False)}`")
    lines.extend(
        [
            "",
            "## By Comment Type",
            "",
            "| type | total | any issue | finding | NHR | line +/-3 | line +/-10 |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for key, item in metrics["by_comment_type"].items():
        lines.append(
            "| {key} | {total} | {any_rate} | {finding_rate} | {nhr_rate} | {line3} | {line10} |".format(
                key=key,
                total=item["total"],
                any_rate=_fmt(item["any_issue_rate"], percent=True),
                finding_rate=_fmt(item["finding_rate"], percent=True),
                nhr_rate=_fmt(item["needs_human_review_rate"], percent=True),
                line3=_fmt(item["line_within_3_rate"], percent=True),
                line10=_fmt(item["line_within_10_rate"], percent=True),
            )
        )
    lines.extend(
        [
            "",
            "## Samples",
            "",
            "| id | type | neg | status | F | NHR | D | line +/-10 | tokens | file |",
            "|---|---|---:|---|---:|---:|---:|---:|---:|---|",
        ]
    )
    for item in metrics["sample_rows"]:
        lines.append(
            "| {sample_id} | {comment_type} | {is_negative} | {status} | {findings} | {needs_human_review} | {discarded} | {line10} | {tokens} | {file_path} |".format(
                sample_id=item["sample_id"],
                comment_type=item["comment_type"],
                is_negative=item["is_negative"],
                status=item["status"],
                findings=item["findings"],
                needs_human_review=item["needs_human_review"],
                discarded=item["discarded"],
                line10=item["line_within_10"],
                tokens=f"{item['token_in']}/{item['token_out']}",
                file_path=str(item["file_path"]).replace("|", "\\|"),
            )
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- `positive_*` treats human-commented chunks as weak positives.",
            "- `negative_*` treats no-comment chunks as weak negatives; these are not guaranteed to be bug-free.",
            "- Line proximity compares emitted issue line against the dataset's human `comment_line` for positive samples.",
        ]
    )
    (work_dir / "metrics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _rate(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return round(numerator / denominator, 4)


def _mean(values: list[int]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def _percentile(values: list[int], percentile: int) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    index = math.ceil((percentile / 100) * len(ordered)) - 1
    return ordered[max(0, min(index, len(ordered) - 1))]


def _fmt(value: object, *, percent: bool = False) -> str:
    if isinstance(value, float) and percent:
        return f"{value:.2%}"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _is_rate_key(key: str) -> bool:
    return "_rate" in key or key in {
        "success_rate",
        "fallback_rate",
    }


if __name__ == "__main__":
    raise SystemExit(main())
