from __future__ import annotations

from shop.models import OrderItem
from shop.service import create_order


def main() -> None:
    order = create_order("debug", [OrderItem("demo", 1, 2500)])
    print(order)


if __name__ == "__main__":
    main()

