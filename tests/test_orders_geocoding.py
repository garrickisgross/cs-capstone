import unittest
from unittest.mock import Mock

import requests

from app.db.in_memory import InMemoryStorage
from app.schemas.orders import CreateOrderInput, StoredOrder
from app.services.geocoding import GeocodingError, NominatimGeocoder
from app.services.optimization import (
    OptimizationService,
    build_haversine_distance_matrix,
    calculate_open_route_distance,
    haversine_distance_miles,
    two_opt_open_route,
)
from app.services.orders import OrdersService


def build_stored_order(
    order_id: str,
    latitude: float,
    longitude: float,
    optimized: bool = False,
) -> StoredOrder:
    return StoredOrder(
        id=order_id,
        address=f"{order_id} Main St",
        city="Dallas",
        st="TX",
        description="",
        latitude=latitude,
        longitude=longitude,
        optimized=optimized,
    )


class NominatimGeocoderTests(unittest.TestCase):
    def test_uses_expected_request_shape(self) -> None:
        session = Mock()
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "features": [
                {
                    "geometry": {
                        "coordinates": [-96.797, 32.7767],
                    }
                }
            ]
        }
        session.get.return_value = response

        geocoder = NominatimGeocoder(session=session)
        result = geocoder.geocode_address("123 Main St", "Dallas", "TX")

        self.assertEqual(result.latitude, 32.7767)
        self.assertEqual(result.longitude, -96.797)
        session.get.assert_called_once_with(
            "https://nominatim.openstreetmap.org/search",
            params={
                "street": "123 Main St",
                "city": "Dallas",
                "state": "TX",
                "countrycodes": "us",
                "format": "geocodejson",
                "limit": 1,
                "accept-language": "en",
            },
            headers={"User-Agent": "cs-capstone/1.0 (student project geocoder)"},
            timeout=10,
        )

    def test_raises_for_no_results(self) -> None:
        session = Mock()
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"features": []}
        session.get.return_value = response

        geocoder = NominatimGeocoder(session=session)

        with self.assertRaises(GeocodingError):
            geocoder.geocode_address("404 Missing St", "Dallas", "TX")

    def test_raises_for_upstream_request_error(self) -> None:
        session = Mock()
        session.get.side_effect = requests.Timeout("timed out")

        geocoder = NominatimGeocoder(session=session)

        with self.assertRaises(GeocodingError):
            geocoder.geocode_address("123 Main St", "Dallas", "TX")


class OrdersServiceTests(unittest.TestCase):
    def test_create_order_stores_coordinates(self) -> None:
        geocoder = Mock()
        geocoder.geocode_address.return_value.latitude = 32.7767
        geocoder.geocode_address.return_value.longitude = -96.797

        storage = InMemoryStorage()
        service = OrdersService(storage, geocoder)

        result = service.create_order(
            CreateOrderInput(
                address="123 Main St",
                city="Dallas",
                st="TX",
                description="Leave at front desk",
            )
        )

        self.assertTrue(result.success)
        stored_orders = storage.list_orders()
        self.assertEqual(len(stored_orders), 1)
        self.assertEqual(stored_orders[0].latitude, 32.7767)
        self.assertEqual(stored_orders[0].longitude, -96.797)
        self.assertFalse(stored_orders[0].optimized)

    def test_create_order_returns_error_when_geocoding_fails(self) -> None:
        geocoder = Mock()
        geocoder.geocode_address.side_effect = GeocodingError("no match")

        storage = InMemoryStorage()
        service = OrdersService(storage, geocoder)

        result = service.create_order(
            CreateOrderInput(
                address="404 Missing St",
                city="Dallas",
                st="TX",
            )
        )

        self.assertFalse(result.success)
        self.assertEqual(result.message, "Could not find coordinates for that address.")
        self.assertEqual(storage.list_orders(), [])

    def test_optimization_service_exposes_coordinates(self) -> None:
        geocoder = Mock()
        geocoder.geocode_address.return_value.latitude = 32.7767
        geocoder.geocode_address.return_value.longitude = -96.797

        storage = InMemoryStorage()
        orders_service = OrdersService(storage, geocoder)
        optimization_service = OptimizationService(storage)

        orders_service.create_order(
            CreateOrderInput(
                address="123 Main St",
                city="Dallas",
                st="TX",
            )
        )

        orders = optimization_service.build_optimized_orders_list().orders

        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].latitude, 32.7767)
        self.assertEqual(orders[0].longitude, -96.797)
        self.assertTrue(orders[0].optimized)
        self.assertEqual(orders[0].stop_number, 1)


class OptimizationAlgorithmTests(unittest.TestCase):
    def test_haversine_distance_is_zero_for_same_point(self) -> None:
        self.assertEqual(haversine_distance_miles(32.7767, -96.797, 32.7767, -96.797), 0.0)

    def test_distance_matrix_is_symmetric_with_zero_diagonal(self) -> None:
        orders = [
            build_stored_order("a", 32.7767, -96.797),
            build_stored_order("b", 29.7604, -95.3698),
            build_stored_order("c", 30.2672, -97.7431),
        ]

        distance_matrix = build_haversine_distance_matrix(orders)

        self.assertEqual(distance_matrix[0][0], 0.0)
        self.assertEqual(distance_matrix[1][1], 0.0)
        self.assertEqual(distance_matrix[2][2], 0.0)
        self.assertEqual(distance_matrix[0][1], distance_matrix[1][0])
        self.assertEqual(distance_matrix[0][2], distance_matrix[2][0])
        self.assertEqual(distance_matrix[1][2], distance_matrix[2][1])

    def test_two_opt_improves_crossing_route(self) -> None:
        distance_matrix = [
            [0.0, 8.0, 1.0, 7.0],
            [8.0, 0.0, 7.0, 1.0],
            [1.0, 7.0, 0.0, 8.0],
            [7.0, 1.0, 8.0, 0.0],
        ]

        original_route = [0, 1, 2, 3]
        optimized_route = two_opt_open_route(original_route, distance_matrix)

        self.assertEqual(optimized_route, [0, 2, 1, 3])
        self.assertLess(
            calculate_open_route_distance(optimized_route, distance_matrix),
            calculate_open_route_distance(original_route, distance_matrix),
        )

    def test_two_opt_leaves_already_good_route_unchanged(self) -> None:
        distance_matrix = [
            [0.0, 1.0, 2.0],
            [1.0, 0.0, 1.0],
            [2.0, 1.0, 0.0],
        ]

        route = [0, 1, 2]

        self.assertEqual(two_opt_open_route(route, distance_matrix), route)

    def test_two_opt_handles_empty_and_single_order_routes(self) -> None:
        self.assertEqual(two_opt_open_route([], []), [])
        self.assertEqual(two_opt_open_route([0], [[0.0]]), [0])


class OptimizationServiceTests(unittest.TestCase):
    def test_build_optimize_page_only_shows_unoptimized_orders(self) -> None:
        storage = InMemoryStorage()
        storage.add_order(build_stored_order("current", 32.7767, -96.797, optimized=False))
        storage.add_order(build_stored_order("done", 29.7604, -95.3698, optimized=True))

        page_data = OptimizationService(storage).build_optimize_page()

        self.assertEqual([order.id for order in page_data.orders_list.orders], ["current"])
        self.assertFalse(page_data.orders_list.orders[0].optimized)

    def test_build_optimized_orders_list_marks_batch_and_returns_summary(self) -> None:
        storage = InMemoryStorage()
        storage.add_order(build_stored_order("a", 0.0, 0.0))
        storage.add_order(build_stored_order("b", 0.0, 3.0))
        storage.add_order(build_stored_order("c", 0.0, 1.0))
        storage.add_order(build_stored_order("d", 0.0, 2.0))
        storage.add_order(build_stored_order("done", 10.0, 10.0, optimized=True))

        orders_list = OptimizationService(storage).build_optimized_orders_list()

        self.assertEqual({order.id for order in orders_list.orders}, {"a", "b", "c", "d"})
        self.assertNotEqual([order.id for order in orders_list.orders], ["a", "b", "c", "d"])
        self.assertEqual([order.stop_number for order in orders_list.orders], [1, 2, 3, 4])
        self.assertTrue(all(order.optimized for order in orders_list.orders))
        self.assertIsNotNone(orders_list.summary)
        self.assertEqual(orders_list.summary.algorithm, "Haversine + 2-opt")
        self.assertEqual(orders_list.summary.order_count, 4)
        self.assertLessEqual(
            orders_list.summary.optimized_distance,
            orders_list.summary.original_distance,
        )
        self.assertEqual(orders_list.summary.distance_saved, round(
            orders_list.summary.original_distance - orders_list.summary.optimized_distance,
            2,
        ))
        self.assertEqual(storage.list_unoptimized_orders(), [])
        self.assertTrue(all(order.optimized for order in storage.list_orders()))

    def test_second_optimization_run_skips_already_optimized_batch(self) -> None:
        storage = InMemoryStorage()
        storage.add_order(build_stored_order("a", 32.7767, -96.797))
        storage.add_order(build_stored_order("b", 29.7604, -95.3698))

        service = OptimizationService(storage)
        first_result = service.build_optimized_orders_list()
        second_result = service.build_optimized_orders_list()

        self.assertEqual(len(first_result.orders), 2)
        self.assertEqual(second_result.orders, [])
        self.assertIsNotNone(second_result.summary)
        self.assertEqual(second_result.summary.order_count, 0)
        self.assertEqual(second_result.summary.original_distance, 0.0)
        self.assertEqual(second_result.summary.optimized_distance, 0.0)
        self.assertEqual(second_result.summary.distance_saved, 0.0)


if __name__ == "__main__":
    unittest.main()
