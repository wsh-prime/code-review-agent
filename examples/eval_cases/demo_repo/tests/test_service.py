from __future__ import annotations

import pytest

from shop.models import OrderItem
from shop.service import cancel_order, create_order


def test_create_order_prices_items() -> None:
    order = create_order(
        "cust_123",
        [OrderItem(sku="sku_1", quantity=2, unit_price_cents=750)],
    )

    assert order.total_cents == 1500
    assert order.status == "created"


def test_create_order_rejects_tiny_orders() -> None:
    with pytest.raises(ValueError):
        create_order("cust_123", [OrderItem(sku="sku_1", quantity=1, unit_price_cents=50)])


def test_cancel_order_marks_status() -> None:
    order = create_order(
        "cust_123",
        [OrderItem(sku="sku_1", quantity=2, unit_price_cents=750)],
    )

    assert cancel_order(order).status == "cancelled"

