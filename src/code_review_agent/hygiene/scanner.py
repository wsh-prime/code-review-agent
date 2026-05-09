"""Read-only repository scanning for Project Hygiene Review."""

from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path


DEFAULT_IGNORED_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".conda",
        ".cache",
        ".checkpoints",
        ".ipynb_checkpoints",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        ".tmp",
        "artifacts",
        "build",
        "checkpoints",
        "dist",
        "htmlcov",
        "log",
        "logs",
        "node_modules",
        "output",
        "outputs",
        "reports",
        "temp",
        "tmp",
        "test_tmp",
        "venv",
    }
)

DEFAULT_IGNORED_FILE_PATTERNS = frozenset(
    {
        "*.checkpoint",
        "*.ckpt",
        "*.diff",
        "*.log",
        "*.patch",
        "*.tmp",
        ".coverage",
        "coverage.xml",
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
    ignored_file_patterns: set[str] | frozenset[str] = DEFAULT_IGNORED_FILE_PATTERNS,
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
    gitignore_rules = _load_gitignore_rules(root)
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if _is_ignored_path(relative, ignored_dirs):
            continue
        if _matches_ignored_file_pattern(relative, ignored_file_patterns):
            continue
        if _is_gitignored(relative, gitignore_rules):
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


def _matches_ignored_file_pattern(
    relative: Path, ignored_file_patterns: set[str] | frozenset[str]
) -> bool:
    relative_posix = relative.as_posix()
    name = relative.name
    return any(
        fnmatch(name, pattern) or fnmatch(relative_posix, pattern)
        for pattern in ignored_file_patterns
    )


@dataclass(frozen=True, slots=True)
class _GitignoreRule:
    pattern: str
    negated: bool
    directory_only: bool
    anchored: bool
    has_slash: bool


def _load_gitignore_rules(root: Path) -> list[_GitignoreRule]:
    gitignore = root / ".gitignore"
    try:
        lines = gitignore.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []

    rules: list[_GitignoreRule] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("\\#"):
            line = line[1:]

        negated = line.startswith("!")
        if negated:
            line = line[1:].strip()
        if not line:
            continue

        anchored = line.startswith("/")
        if anchored:
            line = line[1:]
        directory_only = line.endswith("/")
        if directory_only:
            line = line.rstrip("/")
        if not line:
            continue

        rules.append(
            _GitignoreRule(
                pattern=line,
                negated=negated,
                directory_only=directory_only,
                anchored=anchored,
                has_slash="/" in line,
            )
        )
    return rules


def _is_gitignored(relative: Path, rules: list[_GitignoreRule]) -> bool:
    ignored = False
    for rule in rules:
        if _matches_gitignore_rule(relative, rule):
            ignored = not rule.negated
    return ignored


def _matches_gitignore_rule(relative: Path, rule: _GitignoreRule) -> bool:
    relative_posix = relative.as_posix()
    parts = relative.parts

    if rule.directory_only:
        return _matches_directory_rule(relative_posix, parts, rule)
    if rule.anchored:
        return fnmatch(relative_posix, rule.pattern)
    if rule.has_slash:
        return fnmatch(relative_posix, rule.pattern) or fnmatch(
            relative_posix, f"*/{rule.pattern}"
        )
    return fnmatch(relative.name, rule.pattern) or any(
        fnmatch(part, rule.pattern) for part in parts
    )


def _matches_directory_rule(
    relative_posix: str, parts: tuple[str, ...], rule: _GitignoreRule
) -> bool:
    pattern = rule.pattern.rstrip("/")
    if rule.anchored:
        return relative_posix == pattern or relative_posix.startswith(f"{pattern}/")
    if rule.has_slash:
        return (
            relative_posix == pattern
            or relative_posix.startswith(f"{pattern}/")
            or f"/{pattern}/" in f"/{relative_posix}/"
        )
    return any(part == pattern or fnmatch(part, pattern) for part in parts[:-1])


def _looks_binary(path: Path) -> bool:
    sample = path.read_bytes()[:1024]
    return b"\0" in sample


def _read_text_sample(path: Path, content_bytes: int) -> str:
    raw = path.read_bytes()[:content_bytes]
    return raw.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
