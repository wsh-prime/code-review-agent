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
