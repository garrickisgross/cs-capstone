from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

from ..db.base import StorageInterface
from ..schemas.optimization import (
    OptimizationOrderItem,
    OptimizationOrdersListData,
    OptimizationPageData,
    OptimizationSummaryData,
)
from ..schemas.orders import StoredOrder

EARTH_RADIUS_MILES = 3958.7613


def haversine_distance_miles(
    latitude_a: float,
    longitude_a: float,
    latitude_b: float,
    longitude_b: float,
) -> float:
    if latitude_a == latitude_b and longitude_a == longitude_b:
        return 0.0

    latitude_a_radians = radians(latitude_a)
    latitude_b_radians = radians(latitude_b)
    latitude_delta = radians(latitude_b - latitude_a)
    longitude_delta = radians(longitude_b - longitude_a)

    haversine_value = (
        sin(latitude_delta / 2) ** 2
        + cos(latitude_a_radians)
        * cos(latitude_b_radians)
        * sin(longitude_delta / 2) ** 2
    )
    return 2 * EARTH_RADIUS_MILES * asin(sqrt(haversine_value))


def build_haversine_distance_matrix(orders: list[StoredOrder]) -> list[list[float]]:
    order_count = len(orders)
    matrix = [[0.0 for _ in range(order_count)] for _ in range(order_count)]

    for source_index in range(order_count):
        for target_index in range(source_index + 1, order_count):
            distance = haversine_distance_miles(
                orders[source_index].latitude,
                orders[source_index].longitude,
                orders[target_index].latitude,
                orders[target_index].longitude,
            )
            matrix[source_index][target_index] = distance
            matrix[target_index][source_index] = distance

    return matrix


def calculate_open_route_distance(
    route_order: list[int],
    distance_matrix: list[list[float]],
) -> float:
    total_distance = 0.0
    for source_index, target_index in zip(route_order, route_order[1:]):
        total_distance += distance_matrix[source_index][target_index]
    return total_distance


def two_opt_open_route(
    route_order: list[int],
    distance_matrix: list[list[float]],
) -> list[int]:
    best_route = list(route_order)
    best_distance = calculate_open_route_distance(best_route, distance_matrix)

    while True:
        improvement_found = False
        for start_index in range(len(best_route) - 1):
            for end_index in range(start_index + 1, len(best_route)):
                candidate_route = (
                    best_route[:start_index]
                    + list(reversed(best_route[start_index : end_index + 1]))
                    + best_route[end_index + 1 :]
                )
                candidate_distance = calculate_open_route_distance(
                    candidate_route,
                    distance_matrix,
                )
                if candidate_distance + 1e-9 < best_distance:
                    best_route = candidate_route
                    best_distance = candidate_distance
                    improvement_found = True
                    break
            if improvement_found:
                break
        if not improvement_found:
            return best_route


class OptimizationService:
    def __init__(self, storage: StorageInterface) -> None:
        self._storage = storage

    def build_optimize_page(self) -> OptimizationPageData:
        return OptimizationPageData(
            orders_list=self.build_orders_list(
                title="Current Orders",
                orders=self._storage.list_unoptimized_orders(),
                empty_message="No unoptimized orders are available.",
            ),
            optimize_url="/optimize/orders",
        )

    def build_optimized_orders_list(self) -> OptimizationOrdersListData:
        unoptimized_orders = self._storage.list_unoptimized_orders()
        original_route = list(range(len(unoptimized_orders)))
        distance_matrix = build_haversine_distance_matrix(unoptimized_orders)
        optimized_route = two_opt_open_route(original_route, distance_matrix)
        original_distance = calculate_open_route_distance(
            original_route,
            distance_matrix,
        )
        optimized_distance = calculate_open_route_distance(
            optimized_route,
            distance_matrix,
        )
        rounded_original_distance = round(original_distance, 2)
        rounded_optimized_distance = round(optimized_distance, 2)

        self._storage.mark_orders_optimized([order.id for order in unoptimized_orders])

        optimized_orders = [unoptimized_orders[index] for index in optimized_route]
        return self.build_orders_list(
            title="Optimized Orders",
            orders=optimized_orders,
            optimized_flag=True,
            include_stop_numbers=True,
            summary=OptimizationSummaryData(
                algorithm="Haversine + 2-opt",
                order_count=len(optimized_orders),
                original_distance=rounded_original_distance,
                optimized_distance=rounded_optimized_distance,
                distance_saved=round(
                    max(rounded_original_distance - rounded_optimized_distance, 0.0),
                    2,
                ),
            ),
            empty_message="No unoptimized orders are available.",
        )

    def build_orders_list(
        self,
        title: str,
        orders: list[StoredOrder],
        optimized_flag: bool | None = None,
        include_stop_numbers: bool = False,
        summary: OptimizationSummaryData | None = None,
        empty_message: str = "No orders available.",
    ) -> OptimizationOrdersListData:
        return OptimizationOrdersListData(
            title=title,
            summary=summary,
            empty_message=empty_message,
            orders=[
                OptimizationOrderItem(
                    id=order.id,
                    address=order.address,
                    city=order.city,
                    st=order.st,
                    description=order.description,
                    latitude=order.latitude,
                    longitude=order.longitude,
                    optimized=order.optimized if optimized_flag is None else optimized_flag,
                    stop_number=index if include_stop_numbers else None,
                )
                for index, order in enumerate(orders, start=1)
            ],
        )
