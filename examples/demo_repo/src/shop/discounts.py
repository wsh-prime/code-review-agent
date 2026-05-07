"""Discount and pricing helpers for the demo shop."""

from __future__ import annotations

from .models import OrderItem


def calculate_subtotal(items: list[OrderItem]) -> int:
    """Return the sum of all item totals."""

    return sum(item.total_cents for item in items)


def apply_discount(subtotal_cents: int, coupon: str | None = None) -> int:
    """Apply a small fixed discount for known coupons."""

    if coupon == "WELCOME10":
        return max(subtotal_cents - 1000, 0)
    return subtotal_cents


def loyalty_multiplier(customer_tier: str) -> float:
    """Return the loyalty multiplier for a customer tier."""

    if customer_tier == "gold":
        return 0.9
    if customer_tier == "silver":
        return 0.95
    return 1.0


def tax_cents(total_cents: int) -> int:
    """Return a simple tax estimate."""

    return round(total_cents * 0.08)


def coupon_label(coupon: str | None) -> str:
    """Return a display label for a coupon."""

    return coupon or "none"


def estimate_shipping_days(total_cents: int) -> int:
    if total_cents >= 10_000:
        return 2
    return 5

