from ..db.base import StorageInterface
from ..schemas.optimization import (
    OptimizationOrderItem,
    OptimizationOrdersListData,
    OptimizationPageData,
)


class OptimizationService:
    def __init__(self, storage: StorageInterface) -> None:
        self._storage = storage

    def build_optimize_page(self) -> OptimizationPageData:
        return OptimizationPageData(
            orders_list=self.build_orders_list(title="Current Orders"),
            optimize_url="/optimize/orders",
        )

    def build_optimized_orders_list(self) -> OptimizationOrdersListData:
        return self.build_orders_list(title="Optimized Orders")

    def build_orders_list(self, title: str) -> OptimizationOrdersListData:
        return OptimizationOrdersListData(
            title=title,
            orders=[
                OptimizationOrderItem(
                    id=order.id,
                    address=order.address,
                    city=order.city,
                    st=order.st,
                    description=order.description,
                    latitude=order.latitude,
                    longitude=order.longitude,
                    route_id=order.route_id,
                )
                for order in self._storage.list_orders()
            ],
        )
