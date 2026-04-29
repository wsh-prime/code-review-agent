from __future__ import annotations

from pathlib import Path

from code_review_agent.context.test_discovery import discover_related_tests
from code_review_agent.models import PythonModuleSummary, SymbolSummary


def test_discovers_related_tests_by_path_import_and_symbol(tmp_path: Path) -> None:
    (tmp_path / "src" / "shop").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    (tmp_path / "src" / "shop" / "service.py").write_text(
        "def create_order():\n    return 'ok'\n",
        encoding="utf-8",
    )
    (tmp_path / "src" / "shop" / "discounts.py").write_text(
        "def apply_discount():\n    return 1\n",
        encoding="utf-8",
    )
    (tmp_path / "src" / "shop" / "inventory.py").write_text(
        "def reserve_stock():\n    return None\n",
        encoding="utf-8",
    )
    (tmp_path / "tests" / "test_service.py").write_text(
        "from shop.service import create_order\n",
        encoding="utf-8",
    )
    (tmp_path / "tests" / "test_discounts_behavior.py").write_text(
        "from src.shop.discounts import apply_discount\n",
        encoding="utf-8",
    )
    (tmp_path / "tests" / "test_stock.py").write_text(
        "def test_stock():\n    assert reserve_stock() is None\n",
        encoding="utf-8",
    )

    summaries = [
        PythonModuleSummary(
            path="src/shop/inventory.py",
            module_docstring=None,
            imports=[],
            functions=[
                SymbolSummary(
                    path="src/shop/inventory.py",
                    symbol_type="function",
                    name="reserve_stock",
                    qualified_name="reserve_stock",
                    line_start=1,
                    line_end=2,
                )
            ],
        )
    ]

    related = discover_related_tests(
        tmp_path,
        [
            "src/shop/service.py",
            "src/shop/discounts.py",
            "src/shop/inventory.py",
            "tests/test_service.py",
            "tests/test_discounts_behavior.py",
            "tests/test_stock.py",
        ],
        summaries,
    )

    assert related["src/shop/service.py"] == ["tests/test_service.py"]
    assert related["src/shop/discounts.py"] == ["tests/test_discounts_behavior.py"]
    assert related["src/shop/inventory.py"] == ["tests/test_stock.py"]
