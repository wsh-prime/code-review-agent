from __future__ import annotations

from shop.discounts import apply_discount, estimate_shipping_days
from shop.models import OrderItem


def test_apply_discount_handles_welcome_coupon() -> None:
    assert apply_discount(2500, "WELCOME10") == 1500


def test_estimate_shipping_days_rewards_large_orders() -> None:
    assert estimate_shipping_days(12_000) == 2


def test_order_item_total_cents() -> None:
    assert OrderItem(sku="sku_1", quantity=3, unit_price_cents=400).total_cents == 1200

