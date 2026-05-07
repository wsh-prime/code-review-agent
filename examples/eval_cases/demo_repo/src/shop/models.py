"""Small order models for the demo shop."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class OrderItem:
    """One purchasable line item."""

    sku: str
    quantity: int
    unit_price_cents: int

    @property
    def total_cents(self) -> int:
        """Return the total price for this line item."""

        return self.quantity * self.unit_price_cents


@dataclass(slots=True)
class Order:
    """A completed order."""

    customer_id: str
    total_cents: int
    status: str = "created"

