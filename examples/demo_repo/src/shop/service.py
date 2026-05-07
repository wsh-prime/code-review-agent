"""Order service for the demo shop."""

from __future__ import annotations

from .discounts import apply_discount, calculate_subtotal
from .models import Order, OrderItem

MINIMUM_ORDER_TOTAL_CENTS = 100


def create_order(
    customer_id: str,
    items: list[OrderItem],
    coupon: str | None = None,
) -> Order:
    """Create an order after pricing and validation."""

    subtotal = calculate_subtotal(items)
    total = apply_discount(subtotal, coupon)
    if total < MINIMUM_ORDER_TOTAL_CENTS:
        raise ValueError("order total is too small")
    return Order(customer_id=customer_id, total_cents=total)


def cancel_order(order: Order) -> Order:
    """Return a cancelled copy of an order."""

    return Order(
        customer_id=order.customer_id,
        total_cents=order.total_cents,
        status="cancelled",
    )

