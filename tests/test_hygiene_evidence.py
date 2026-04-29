"""Tests for hygiene.evidence module."""

from __future__ import annotations

from code_review_agent.hygiene.evidence import collect_evidence, is_safety_guard_triggered
from code_review_agent.hygiene.scanner import ScannedFile
from code_review_agent.models import HygieneEvidence


def _file(path: str, content: str = "") -> ScannedFile:
    return ScannedFile(
        path=path,
        extension="." + path.rsplit(".", 1)[-1] if "." in path else "",
        size_bytes=len(content),
        content_sample=content,
    )


# ---------------------------------------------------------------------------
# collect_evidence
# ---------------------------------------------------------------------------


def test_collect_evidence_returns_one_per_file(tmp_path) -> None:
    files = [_file("src/app.py", ""), _file("README.md", "")]
    evidences = collect_evidence(tmp_path, files)
    assert len(evidences) == 2
    assert {e.path for e in evidences} == {"src/app.py", "README.md"}


def test_imported_by_is_populated(tmp_path) -> None:
    files = [
        _file("src/app.py", "import helper\n"),
        _file("helper.py", "def normalize(): pass\n"),
    ]
    evidences = {e.path: e for e in collect_evidence(tmp_path, files)}
    assert "src/app.py" in evidences["helper.py"].imported_by


def test_referenced_by_tests_is_populated(tmp_path) -> None:
    files = [
        _file("tests/test_app.py", "import src.service\n"),
        _file("src/service.py", "def run(): pass\n"),
    ]
    evidences = {e.path: e for e in collect_evidence(tmp_path, files)}
    assert "tests/test_app.py" in evidences["src/service.py"].referenced_by_tests


def test_declared_in_config_is_populated(tmp_path) -> None:
    files = [
        _file("pyproject.toml", "[tool.mypy]\nmodules = [\"mymodule\"]\n"),
        _file("mymodule.py", ""),
    ]
    evidences = {e.path: e for e in collect_evidence(tmp_path, files)}
    assert "pyproject.toml" in evidences["mymodule.py"].declared_in_config


def test_folder_context_is_read_from_summaries(tmp_path) -> None:
    files = [_file("src/orders/service.py", "")]
    summaries = {"src/orders": {"responsibility": "Order domain logic"}}
    evidences = {e.path: e for e in collect_evidence(tmp_path, files, folder_summaries=summaries)}
    assert evidences["src/orders/service.py"].folder_context == "Order domain logic"


def test_content_sample_is_truncated_to_500(tmp_path) -> None:
    long_content = "x" * 2000
    files = [_file("big.py", long_content)]
    evidences = collect_evidence(tmp_path, files)
    assert len(evidences[0].content_sample) <= 500


def test_no_self_reference_in_imported_by(tmp_path) -> None:
    files = [_file("utils.py", "from utils import helper\n")]
    evidences = {e.path: e for e in collect_evidence(tmp_path, files)}
    assert "utils.py" not in evidences["utils.py"].imported_by


# ---------------------------------------------------------------------------
# is_safety_guard_triggered
# ---------------------------------------------------------------------------


def test_safety_guard_triggered_by_imported_by() -> None:
    ev = HygieneEvidence(
        path="helper.py",
        content_sample="",
        imported_by=["src/app.py"],
    )
    assert is_safety_guard_triggered(ev)


def test_safety_guard_triggered_by_referenced_by_tests() -> None:
    ev = HygieneEvidence(
        path="src/service.py",
        content_sample="",
        referenced_by_tests=["tests/test_service.py"],
    )
    assert is_safety_guard_triggered(ev)


def test_safety_guard_triggered_by_declared_in_config() -> None:
    ev = HygieneEvidence(
        path="mymodule.py",
        content_sample="",
        declared_in_config=["pyproject.toml"],
    )
    assert is_safety_guard_triggered(ev)


def test_safety_guard_triggered_by_core_filename() -> None:
    for name in ("README.md", "pyproject.toml", "LICENSE"):
        ev = HygieneEvidence(path=name, content_sample="")
        assert is_safety_guard_triggered(ev), f"{name} should trigger safety guard"


def test_safety_guard_not_triggered_for_ordinary_script() -> None:
    ev = HygieneEvidence(path="scripts/download_data.py", content_sample="")
    assert not is_safety_guard_triggered(ev)
