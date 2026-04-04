from .base import StorageInterface
from ..schemas.orders import StoredOrder


class InMemoryStorage(StorageInterface):
    def __init__(self) -> None:
        self._orders: list[StoredOrder] = []

    def add_order(self, order: StoredOrder) -> None:
        self._orders.append(order)

    def list_orders(self) -> list[StoredOrder]:
        return list(self._orders)

    def list_unoptimized_orders(self) -> list[StoredOrder]:
        return [order for order in self._orders if not order.optimized]

    def mark_orders_optimized(self, order_ids: list[str]) -> None:
        ids_to_mark = set(order_ids)
        for index, order in enumerate(self._orders):
            if order.id in ids_to_mark:
                self._orders[index] = order.model_copy(update={"optimized": True})
