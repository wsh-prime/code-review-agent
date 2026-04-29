"""Build a minimal machine-readable RepoMap for Python repositories."""

from __future__ import annotations

import ast
from collections import Counter, defaultdict
from pathlib import Path

from code_review_agent.context.test_discovery import discover_related_tests
from code_review_agent.hygiene.scanner import scan_repository
from code_review_agent.models import (
    PythonModuleSummary,
    RepoMap,
    StyleBaseline,
    SymbolSummary,
)


def build_repo_map(repo_path: Path | str) -> RepoMap:
    """Scan a repository and summarize Python files, imports, and symbols."""

    root = Path(repo_path).resolve()
    scanned_files = scan_repository(root)
    files = [scanned.path for scanned in scanned_files]
    python_paths = [path for path in files if path.endswith(".py")]

    modules: list[PythonModuleSummary] = []
    import_map: dict[str, list[str]] = {}

    for relative_path in python_paths:
        summary = _summarize_python_module(root, relative_path)
        if summary is None:
            import_map[relative_path] = []
            continue
        modules.append(summary)
        import_map[relative_path] = summary.imports

    related_tests = discover_related_tests(root, python_paths, modules)

    return RepoMap(
        root=str(root),
        files=files,
        python_modules=modules,
        imports=import_map,
        imported_by=_build_imported_by(import_map, python_paths),
        related_tests=related_tests,
        style_baseline=_build_style_baseline(root, modules, python_paths),
    )


def render_repo_map_markdown(repo_map: RepoMap) -> str:
    """Render a compact Markdown summary for humans."""

    lines = [
        "# Repo Map",
        "",
        "## Summary",
        "",
        f"- Root: `{repo_map.root}`",
        f"- Files scanned: {len(repo_map.files)}",
        f"- Python modules: {len(repo_map.python_modules)}",
        "",
        "## Python Modules",
        "",
        "| File | Imports | Classes | Functions | Methods | Related Tests |",
        "|---|---:|---:|---:|---:|---|",
    ]

    for module in repo_map.python_modules:
        related_tests = ", ".join(
            f"`{path}`" for path in repo_map.related_tests.get(module.path, [])
        )
        lines.append(
            "| "
            f"`{module.path}` | "
            f"{len(module.imports)} | "
            f"{len(module.classes)} | "
            f"{len(module.functions)} | "
            f"{len(module.methods)} | "
            f"{related_tests or '-'} |"
        )

    baseline = repo_map.style_baseline
    if baseline is not None:
        lines.extend(
            [
                "",
                "## Style Baseline",
                "",
                f"- Public function docstring coverage: {baseline.docstring_coverage_ratio:.2f}",
                f"- Dominant import style: `{baseline.dominant_import_style}`",
                f"- Test naming pattern: `{baseline.test_naming_pattern or 'unknown'}`",
                f"- Dominant exception handling: `{baseline.dominant_exception_handling}`",
                f"- Public functions sampled: {baseline.total_public_functions}",
            ]
        )

    lines.append("")
    return "\n".join(lines)


def _summarize_python_module(
    root: Path, relative_path: str
) -> PythonModuleSummary | None:
    path = root / relative_path
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except (OSError, SyntaxError):
        return None

    classes: list[SymbolSummary] = []
    functions: list[SymbolSummary] = []
    methods: list[SymbolSummary] = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes.append(_symbol_from_node(relative_path, "class", node, node.name))
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append(
                        _symbol_from_node(
                            relative_path,
                            "method",
                            child,
                            f"{node.name}.{child.name}",
                        )
                    )
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(_symbol_from_node(relative_path, "function", node, node.name))

    return PythonModuleSummary(
        path=relative_path,
        module_docstring=ast.get_docstring(tree),
        imports=_extract_imports(tree),
        classes=classes,
        functions=functions,
        methods=methods,
    )


def _symbol_from_node(
    path: str,
    symbol_type: str,
    node: ast.AST,
    qualified_name: str,
) -> SymbolSummary:
    name = qualified_name.rsplit(".", 1)[-1]
    line_start = getattr(node, "lineno", 1)
    line_end = getattr(node, "end_lineno", line_start)
    return SymbolSummary(
        path=path,
        symbol_type=symbol_type,
        name=name,
        qualified_name=qualified_name,
        line_start=line_start,
        line_end=line_end,
    )


def _extract_imports(tree: ast.AST) -> list[str]:
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = f"{'.' * node.level}{node.module or ''}"
            for alias in node.names:
                if alias.name == "*":
                    imports.append(f"{module}.*")
                elif module:
                    imports.append(f"{module}.{alias.name}")
                else:
                    imports.append(f"{'.' * node.level}{alias.name}")
    return sorted(set(imports))


def _build_imported_by(
    import_map: dict[str, list[str]], python_paths: list[str]
) -> dict[str, list[str]]:
    module_names_by_path: dict[str, set[str]] = {
        path: _module_name_variants(path) for path in python_paths
    }
    imported_by: dict[str, list[str]] = defaultdict(list)

    for source_path, imports in import_map.items():
        for imported_name in imports:
            normalized = imported_name.lstrip(".")
            for target_path, module_names in module_names_by_path.items():
                if target_path == source_path:
                    continue
                if _import_matches_module(normalized, module_names):
                    imported_by[target_path].append(source_path)

    return {
        path: sorted(set(importers))
        for path, importers in sorted(imported_by.items())
    }


def _module_name_variants(path: str) -> set[str]:
    module_name = Path(path).with_suffix("").as_posix().replace("/", ".")
    variants = {module_name}
    if module_name.startswith("src."):
        variants.add(module_name.removeprefix("src."))
    return variants


def _import_matches_module(import_name: str, module_names: set[str]) -> bool:
    return any(
        import_name == module_name or import_name.startswith(f"{module_name}.")
        for module_name in module_names
    )


def _build_style_baseline(
    root: Path, modules: list[PythonModuleSummary], python_paths: list[str]
) -> StyleBaseline:
    public_symbols = [
        symbol
        for module in modules
        if not _is_test_file_name(module.path)
        for symbol in [*module.functions, *module.methods]
        if not symbol.name.startswith("_")
    ]
    documented = _count_documented_public_functions(root, modules)
    total_public = len(public_symbols)
    docstring_ratio = documented / total_public if total_public else 0.0

    import_styles = Counter(
        "relative" if imported.startswith(".") else "absolute"
        for module in modules
        for imported in module.imports
    )
    dominant_import_style = _dominant_style(import_styles)

    test_patterns = Counter(
        "test_*" if Path(path).name.startswith("test_") else "*_test"
        for path in python_paths
        if _is_test_file_name(path)
    )

    return StyleBaseline(
        docstring_coverage_ratio=round(docstring_ratio, 4),
        dominant_import_style=dominant_import_style,
        test_naming_pattern=(
            test_patterns.most_common(1)[0][0] if test_patterns else None
        ),
        dominant_exception_handling="mixed",
        total_public_functions=total_public,
    )


def _count_documented_public_functions(
    root: Path, modules: list[PythonModuleSummary]
) -> int:
    documented = 0
    for module in modules:
        if _is_test_file_name(module.path):
            continue
        try:
            tree = ast.parse(
                (root / module.path).read_text(encoding="utf-8", errors="replace")
            )
        except (OSError, SyntaxError):
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith("_") and ast.get_docstring(node):
                    documented += 1
            elif isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if not child.name.startswith("_") and ast.get_docstring(child):
                            documented += 1
    return documented


def _dominant_style(styles: Counter[str]) -> str:
    if not styles:
        return "mixed"
    if len(styles) == 1:
        return next(iter(styles))
    return "mixed"


def _is_test_file_name(path: str) -> bool:
    name = Path(path).name
    return name.startswith("test_") or name.endswith("_test.py")
