"""Read-only repository scanning for Project Hygiene Review."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_IGNORED_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        "venv",
    }
)

DEFAULT_BINARY_EXTENSIONS = frozenset(
    {
        ".7z",
        ".bin",
        ".bmp",
        ".dll",
        ".exe",
        ".gif",
        ".ico",
        ".jpeg",
        ".jpg",
        ".pdf",
        ".png",
        ".pyc",
        ".so",
        ".tar",
        ".zip",
    }
)

DEFAULT_MAX_FILE_BYTES = 1_000_000
DEFAULT_CONTENT_BYTES = 4096


@dataclass(slots=True)
class ScannedFile:
    """Lightweight metadata captured without mutating the target repo."""

    path: str
    extension: str
    size_bytes: int
    content_sample: str


def scan_repository(
    repo_path: Path | str,
    *,
    ignored_dirs: set[str] | frozenset[str] = DEFAULT_IGNORED_DIRS,
    binary_extensions: set[str] | frozenset[str] = DEFAULT_BINARY_EXTENSIONS,
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
    content_bytes: int = DEFAULT_CONTENT_BYTES,
) -> list[ScannedFile]:
    """Scan a repository and return text-like file metadata.

    The scanner intentionally skips common cache/build/virtualenv directories,
    binary-like files, and very large files. It only reads small samples and
    never writes to the scanned repository.
    """

    root = Path(repo_path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {root}")

    scanned: list[ScannedFile] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if _is_ignored_path(relative, ignored_dirs):
            continue
        if path.suffix.lower() in binary_extensions:
            continue

        size_bytes = path.stat().st_size
        if size_bytes > max_file_bytes:
            continue
        if _looks_binary(path):
            continue

        content_sample = _read_text_sample(path, content_bytes)
        scanned.append(
            ScannedFile(
                path=relative.as_posix(),
                extension=path.suffix.lower(),
                size_bytes=size_bytes,
                content_sample=content_sample,
            )
        )

    return scanned


def _is_ignored_path(relative: Path, ignored_dirs: set[str] | frozenset[str]) -> bool:
    return any(part in ignored_dirs for part in relative.parts)


def _looks_binary(path: Path) -> bool:
    sample = path.read_bytes()[:1024]
    return b"\0" in sample


def _read_text_sample(path: Path, content_bytes: int) -> str:
    raw = path.read_bytes()[:content_bytes]
    return raw.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
