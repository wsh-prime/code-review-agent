"""HTTP-facing payload helpers for the demo shop."""

from __future__ import annotations


def create_order_payload(customer_id: str, total_cents: int) -> dict[str, object]:
    """Build a response payload for a created order."""

    return {
        "customer_id": customer_id,
        "total_cents": total_cents,
        "status": "created",
    }

