from uuid import uuid4

from ..db.base import StorageInterface
from ..schemas.orders import (
    CreateOrderInput,
    OrderFormElement,
    OrderCreatedMessage,
    OrdersPageData,
    StoredOrder,
)


class OrdersService:
    def __init__(self, storage: StorageInterface) -> None:
        self._storage = storage

    def build_orders_page(self) -> OrdersPageData:
        return OrdersPageData(
            elements=[
                OrderFormElement(
                    name="address",
                    input_type="text",
                    help_text="Enter address for this order",
                ),
                OrderFormElement(
                    name="city",
                    input_type="text",
                    help_text="City",
                ),
                OrderFormElement(
                    name="st",
                    input_type="text",
                    help_text="St",
                ),
                OrderFormElement(
                    name="description",
                    input_type="text",
                    help_text="Optional Description",
                ),
            ],
            url="/create_order",
        )

    def create_order(self, order_input: CreateOrderInput) -> OrderCreatedMessage:
        order = StoredOrder(
            id=str(uuid4()),
            address=order_input.address,
            city=order_input.city,
            st=order_input.st,
            description=order_input.description or "",
        )
        self._storage.add_order(order)
        print([stored_order.to_row() for stored_order in self._storage.list_orders()])
        return OrderCreatedMessage(message="Order created successfully.")
