from __future__ import annotations

from shop.models import OrderItem


def sample_items() -> list[OrderItem]:
    return [OrderItem(sku="demo", quantity=1, unit_price_cents=2500)]

