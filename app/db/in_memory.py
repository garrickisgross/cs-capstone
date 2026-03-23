from .base import StorageInterface
from ..schemas.orders import StoredOrder


class InMemoryStorage(StorageInterface):
    def __init__(self) -> None:
        self._orders: list[StoredOrder] = []

    def add_order(self, order: StoredOrder) -> None:
        self._orders.append(order)

    def list_orders(self) -> list[StoredOrder]:
        return list(self._orders)
