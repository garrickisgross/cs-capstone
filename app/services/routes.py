from ..db.base import StorageInterface
from ..schemas.routes import RoutesPageData


class RoutesService:
    def __init__(self, storage: StorageInterface) -> None:
        self._storage = storage

    def build_routes_page(self) -> RoutesPageData:
        return RoutesPageData(
            data=[order.to_row() for order in self._storage.list_orders()],
        )
