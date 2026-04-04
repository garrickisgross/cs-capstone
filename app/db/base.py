from abc import ABC, abstractmethod

from ..schemas.orders import StoredOrder


class StorageInterface(ABC):
    @abstractmethod
    def add_order(self, order: StoredOrder) -> None:
        pass

    @abstractmethod
    def list_orders(self) -> list[StoredOrder]:
        pass

    @abstractmethod
    def list_unoptimized_orders(self) -> list[StoredOrder]:
        pass

    @abstractmethod
    def mark_orders_optimized(self, order_ids: list[str]) -> None:
        pass
