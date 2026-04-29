from __future__ import annotations

from code_review_agent.hygiene.classifier import (
    classify_files,
    index_classifications_by_path,
)
from code_review_agent.hygiene.scanner import ScannedFile


def test_classify_common_ai_coding_artifacts(tmp_path) -> None:
    files = [
        ScannedFile(
            path="download_data.py",
            extension=".py",
            size_bytes=20,
            content_sample="import requests\nrequests.get('https://example.test/data.csv')\n",
        ),
        ScannedFile(
            path="test_prompt_v2.py",
            extension=".py",
            size_bytes=20,
            content_sample="PROMPT = 'try a prompt experiment'\n",
        ),
        ScannedFile(
            path="todo.md",
            extension=".md",
            size_bytes=20,
            content_sample="- [ ] tighten review pipeline\n",
        ),
        ScannedFile(
            path="README.md",
            extension=".md",
            size_bytes=20,
            content_sample="# Project\n",
        ),
    ]

    classifications = {
        classification.path: classification
        for classification in classify_files(tmp_path, files)
    }

    assert classifications["download_data.py"].category == "data_script"
    assert classifications["test_prompt_v2.py"].category == "experiment"
    assert classifications["todo.md"].category == "todo"
    assert classifications["README.md"].mainline_relevance == "high"
    assert classifications["test_prompt_v2.py"].signals

    indexed = index_classifications_by_path(list(classifications.values()))
    assert indexed["download_data.py"].category == "data_script"


def test_imported_python_file_is_preserved_as_main_code(tmp_path) -> None:
    files = [
        ScannedFile(
            path="src/app.py",
            extension=".py",
            size_bytes=20,
            content_sample="import helper\n\ndef run():\n    return helper.normalize('A')\n",
        ),
        ScannedFile(
            path="helper.py",
            extension=".py",
            size_bytes=20,
            content_sample="def normalize(value):\n    return value.lower()\n",
        ),
    ]

    classifications = {
        classification.path: classification
        for classification in classify_files(tmp_path, files)
    }

    assert classifications["helper.py"].category == "main_code"
    assert classifications["helper.py"].mainline_relevance == "high"
