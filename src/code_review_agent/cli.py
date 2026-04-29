"""Command line interface for Code Review Agent Harness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from code_review_agent.context.repo_map import build_repo_map, render_repo_map_markdown
from code_review_agent.hygiene.classifier import classify_files, classify_files_semantic
from code_review_agent.hygiene.llm_classifier import FakeLLMClassifier
from code_review_agent.hygiene.planner import (
    build_move_suggestions,
    build_move_suggestions_from_semantic,
    build_project_artifacts_draft,
    build_uncertain_queue,
)
from code_review_agent.hygiene.scanner import scan_repository
from code_review_agent.models import ReviewReport
from code_review_agent.review.pipeline import run_review_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="code-review-agent",
        description="Run a local Code Review Agent Harness workflow.",
    )
    subparsers = parser.add_subparsers(dest="command")

    map_parser = subparsers.add_parser(
        "map",
        help="Build a machine-readable RepoMap for a repository.",
    )
    map_parser.add_argument(
        "--repo",
        required=True,
        type=Path,
        help="Path to the repository to analyze.",
    )
    map_parser.add_argument(
        "--out",
        required=True,
        type=Path,
        help="Directory where RepoMap reports will be written.",
    )
    map_parser.set_defaults(handler=run_map_command)

    hygiene_parser = subparsers.add_parser(
        "hygiene",
        help="Scan a repository and output a project hygiene report.",
    )
    hygiene_parser.add_argument(
        "--repo",
        required=True,
        type=Path,
        help="Path to the repository to analyze.",
    )
    hygiene_parser.add_argument(
        "--out",
        required=True,
        type=Path,
        help="Directory where hygiene reports will be written.",
    )
    hygiene_parser.add_argument(
        "--summary",
        type=Path,
        default=None,
        help="Optional path to folder_summaries.json produced by the summary command.",
    )
    hygiene_parser.add_argument(
        "--classifier",
        choices=["rules", "hybrid"],
        default="rules",
        help=(
            "Classification mode. "
            "'rules' uses deterministic path/content signals only. "
            "'hybrid' adds LLM semantic classification on top (uses "
            "FakeLLMClassifier until a real LLM provider is configured)."
        ),
    )
    hygiene_parser.set_defaults(handler=run_hygiene_command)

    review_parser = subparsers.add_parser(
        "review",
        help="Run a rules-only review over a unified diff.",
    )
    review_parser.add_argument(
        "--repo",
        required=True,
        type=Path,
        help="Path to the repository to analyze.",
    )
    review_parser.add_argument(
        "--diff",
        required=True,
        type=Path,
        help="Path to a unified diff or patch file.",
    )
    review_parser.add_argument(
        "--out",
        required=True,
        type=Path,
        help="Directory where review reports will be written.",
    )
    review_parser.add_argument(
        "--repo-map",
        type=Path,
        default=None,
        help="Optional repo_map.json produced by the map command.",
    )
    review_parser.add_argument(
        "--hygiene",
        type=Path,
        default=None,
        help="Optional project_hygiene.json produced by the hygiene command.",
    )
    review_parser.add_argument(
        "--mode",
        choices=["rules", "hybrid-fake", "hybrid-live"],
        default="rules",
        help=(
            "Review mode. Use hybrid-fake to exercise the agent harness "
            "without API calls, or hybrid-live for an OpenAI-compatible backend."
        ),
    )
    review_parser.add_argument(
        "--export-prompts",
        action="store_true",
        help="Write fake review/critic prompt files and redacted input JSON.",
    )
    review_parser.set_defaults(handler=run_review_command)

    return parser


def run_map_command(args: argparse.Namespace) -> int:
    """Build and write a RepoMap report."""

    repo_map = build_repo_map(args.repo)

    args.out.mkdir(parents=True, exist_ok=True)
    json_path = args.out / "repo_map.json"
    markdown_path = args.out / "repo_map.md"
    json_path.write_text(
        json.dumps(repo_map.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    markdown_path.write_text(render_repo_map_markdown(repo_map), encoding="utf-8")

    print("Code Review Agent Harness - map")
    print(f"Repo:           {args.repo}")
    print(f"Out:            {args.out}")
    print(f"Files scanned:  {len(repo_map.files)}")
    print(f"Python modules: {len(repo_map.python_modules)}")
    print(f"Wrote: {json_path}")
    print(f"Wrote: {markdown_path}")
    print("No target repository files were modified.")
    return 0


def run_hygiene_command(args: argparse.Namespace) -> int:
    """Run the Project Hygiene Review workflow."""

    folder_summaries = None
    if args.summary:
        if not args.summary.exists():
            print(f"WARNING: --summary path does not exist: {args.summary}")
        else:
            folder_summaries = json.loads(args.summary.read_text(encoding="utf-8"))
            print(f"Loaded folder summaries: {args.summary}")

    scanned_files = scan_repository(args.repo)

    if args.classifier == "hybrid":
        llm = FakeLLMClassifier()
        classifications, semantic_classifications = classify_files_semantic(
            args.repo, scanned_files, llm, folder_summaries=folder_summaries
        )
        suggestions = build_move_suggestions_from_semantic(
            args.repo, semantic_classifications
        )
        uncertain_queue = build_uncertain_queue(semantic_classifications)
    else:
        classifications = classify_files(args.repo, scanned_files)
        suggestions = build_move_suggestions(args.repo, classifications)
        semantic_classifications = []
        uncertain_queue = []

    artifacts_draft = build_project_artifacts_draft(classifications, suggestions)

    report = ReviewReport(
        summary={
            "classifier": args.classifier,
            "scanned_file_count": len(scanned_files),
            "classification_count": len(classifications),
            "semantic_classification_count": len(semantic_classifications),
            "move_suggestion_count": len(suggestions),
            "uncertain_queue_count": len(uncertain_queue),
            "target_repo_modified": False,
        },
        file_classifications=classifications,
        move_suggestions=suggestions,
        semantic_classifications=semantic_classifications,
        uncertain_queue=uncertain_queue,
        project_artifacts_draft=artifacts_draft,
    )

    args.out.mkdir(parents=True, exist_ok=True)
    hygiene_json_path = args.out / "project_hygiene.json"
    artifacts_path = args.out / "PROJECT_ARTIFACTS.md"
    hygiene_json_path.write_text(
        json.dumps(report.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    artifacts_path.write_text(artifacts_draft, encoding="utf-8")

    if uncertain_queue:
        uncertain_path = args.out / "uncertain_queue.md"
        uncertain_path.write_text(
            _render_uncertain_queue(uncertain_queue), encoding="utf-8"
        )
        print(f"Wrote: {uncertain_path}")

    print("Code Review Agent Harness - hygiene")
    print(f"Repo:       {args.repo}")
    print(f"Out:        {args.out}")
    print(f"Classifier: {args.classifier}")
    print(f"Scanned files:         {len(scanned_files)}")
    print(f"Move suggestions:      {len(suggestions)}")
    print(f"Uncertain queue:       {len(uncertain_queue)}")
    print(f"Wrote: {hygiene_json_path}")
    print(f"Wrote: {artifacts_path}")
    print("No target repository files were modified.")
    return 0


def run_review_command(args: argparse.Namespace) -> int:
    """Run the rules-only review pipeline."""

    report = run_review_pipeline(
        args.repo,
        args.diff,
        args.out,
        repo_map_path=args.repo_map,
        hygiene_path=args.hygiene,
        mode=args.mode,
        export_prompts=args.export_prompts,
    )

    json_path = args.out / "review_report.json"
    markdown_path = args.out / "review_report.md"
    summary = report["summary"]
    print("Code Review Agent Harness - review")
    print(f"Repo:                {args.repo}")
    print(f"Diff:                {args.diff}")
    print(f"Out:                 {args.out}")
    print(f"Mode:                {args.mode}")
    print(f"Changed files:       {summary['changed_file_count']}")
    print(f"Risk signals:        {summary['risk_signal_count']}")
    print(f"Findings:            {summary['finding_count']}")
    print(f"Needs human review:  {summary['needs_human_review_count']}")
    print(f"Discarded:           {summary.get('discarded_count', 0)}")
    print(f"Wrote: {json_path}")
    print(f"Wrote: {markdown_path}")
    if args.export_prompts:
        print(f"Wrote prompts: {args.out / 'prompts'}")
    print("No target repository files were modified.")
    return 0


def _render_uncertain_queue(uncertain: list) -> str:
    lines = [
        "# Uncertain Queue",
        "",
        "> Files where the classifier could not make a confident determination.",
        "> Review each file and decide: keep, move, or delete.",
        "",
        "| File | Artifact Type | Confidence | Reason |",
        "|---|---|---:|---|",
    ]
    for sc in uncertain:
        reason = sc.reason.replace("|", "\\|")
        lines.append(
            f"| `{sc.path}` | `{sc.artifact_type}` | {sc.confidence:.2f} | {reason} |"
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "handler"):
        parser.print_help()
        return 0

    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
