from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from code_review_agent.context.repo_map import build_repo_map, render_repo_map_markdown


def test_build_repo_map_extracts_imports_symbols_and_related_tests(
    tmp_path: Path,
) -> None:
    _write_sample_repo(tmp_path)

    repo_map = build_repo_map(tmp_path)

    service = next(
        module
        for module in repo_map.python_modules
        if module.path == "src/shop/service.py"
    )
    assert service.module_docstring == "Order service."
    assert "dataclasses.dataclass" in service.imports
    assert "shop.models.Order" in service.imports
    assert service.classes[0].qualified_name == "OrderService"
    assert service.functions[0].qualified_name == "normalize_name"
    assert service.methods[0].qualified_name == "OrderService.create"
    assert service.methods[0].line_start < service.methods[0].line_end
    assert repo_map.related_tests["src/shop/service.py"] == [
        "tests/test_service.py"
    ]
    assert repo_map.style_baseline is not None
    assert repo_map.style_baseline.total_public_functions == 2
    assert repo_map.style_baseline.docstring_coverage_ratio == 0.5


def test_build_repo_map_skips_unparseable_python_without_crashing(
    tmp_path: Path,
) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "broken.py").write_text("def broken(:\n", encoding="utf-8")

    repo_map = build_repo_map(tmp_path)

    assert "src/broken.py" in repo_map.files
    assert repo_map.python_modules == []
    assert repo_map.imports["src/broken.py"] == []


def test_render_repo_map_markdown_includes_core_sections(tmp_path: Path) -> None:
    _write_sample_repo(tmp_path)
    repo_map = build_repo_map(tmp_path)

    markdown = render_repo_map_markdown(repo_map)

    assert "# Repo Map" in markdown
    assert "`src/shop/service.py`" in markdown
    assert "Style Baseline" in markdown


def test_map_cli_writes_json_and_markdown(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    out = tmp_path / "out"
    _write_sample_repo(repo)
    project_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root / "src")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "code_review_agent.cli",
            "map",
            "--repo",
            str(repo),
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
    data = json.loads((out / "repo_map.json").read_text(encoding="utf-8"))
    assert data["python_modules"][0]["path"] == "src/shop/service.py"
    assert (out / "repo_map.md").exists()


def _write_sample_repo(root: Path) -> None:
    (root / "src" / "shop").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "src" / "shop" / "service.py").write_text(
        '"""Order service."""\n'
        "from dataclasses import dataclass\n"
        "from shop.models import Order\n\n"
        "class OrderService:\n"
        "    def create(self, name: str) -> str:\n"
        "        return normalize_name(name)\n\n"
        "def normalize_name(name: str) -> str:\n"
        '    """Normalize a user-visible order name."""\n'
        "    return name.strip().lower()\n",
        encoding="utf-8",
    )
    (root / "tests" / "test_service.py").write_text(
        "from shop.service import OrderService\n\n"
        "def test_create():\n"
        "    assert OrderService().create(' A ') == 'a'\n",
        encoding="utf-8",
    )
