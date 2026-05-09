from __future__ import annotations

from code_review_agent.hygiene.scanner import scan_repository


def test_scan_repository_ignores_cache_build_and_binary_files(tmp_path) -> None:
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / ".git").mkdir()
    (repo / "node_modules").mkdir()
    (repo / "src" / "app.py").write_text("print('hello')\n", encoding="utf-8")
    (repo / ".git" / "config").write_text("[core]\n", encoding="utf-8")
    (repo / "node_modules" / "pkg.js").write_text("console.log('x')\n", encoding="utf-8")
    (repo / "image.png").write_bytes(b"\x89PNG\x00binary")

    scanned = scan_repository(repo)

    assert [file.path for file in scanned] == ["src/app.py"]
    assert scanned[0].extension == ".py"
    assert scanned[0].content_sample == "print('hello')\n"


def test_scan_repository_respects_gitignore_with_negation(tmp_path) -> None:
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "notes").mkdir()
    (repo / ".gitignore").write_text(
        "notes/\n"
        "*.secret\n"
        ".env.*\n"
        "!.env.example\n",
        encoding="utf-8",
    )
    (repo / "src" / "app.py").write_text("print('hello')\n", encoding="utf-8")
    (repo / "notes" / "draft.md").write_text("draft\n", encoding="utf-8")
    (repo / "token.secret").write_text("secret\n", encoding="utf-8")
    (repo / ".env.local").write_text("SECRET=x\n", encoding="utf-8")
    (repo / ".env.example").write_text("SECRET=\n", encoding="utf-8")

    paths = [file.path for file in scan_repository(repo)]

    assert paths == [".env.example", ".gitignore", "src/app.py"]


def test_scan_repository_ignores_generated_run_artifacts(tmp_path) -> None:
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / ".conda" / "Lib").mkdir(parents=True)
    (repo / "logs").mkdir()
    (repo / "checkpoints").mkdir()
    (repo / "outputs" / "runs" / "run1").mkdir(parents=True)
    (repo / ".tmp").mkdir()
    (repo / "src" / "app.py").write_text("print('hello')\n", encoding="utf-8")
    (repo / ".conda" / "Lib" / "typing.py").write_text("class Any:\n    pass\n", encoding="utf-8")
    (repo / "outputs" / "runs" / "run1" / "review_report.json").write_text("{}", encoding="utf-8")
    (repo / ".tmp" / "changes.patch").write_text("diff --git a/x b/x\n", encoding="utf-8")
    (repo / "changes.patch").write_text("diff --git a/x b/x\n", encoding="utf-8")
    (repo / "run.log").write_text("slow call\n", encoding="utf-8")
    (repo / "review.checkpoint").write_text("{}", encoding="utf-8")
    (repo / "logs" / "run.log").write_text("slow call\n", encoding="utf-8")
    (repo / "checkpoints" / "review.json").write_text("{}", encoding="utf-8")

    paths = [file.path for file in scan_repository(repo)]

    assert paths == ["src/app.py"]
