from abc import ABC, abstractmethod

from ..schemas.orders import StoredOrder


class StorageInterface(ABC):
    @abstractmethod
    def add_order(self, order: StoredOrder) -> None:
        pass

    @abstractmethod
    def list_orders(self) -> list[StoredOrder]:
        pass
