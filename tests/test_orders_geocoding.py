import unittest
from unittest.mock import Mock

import requests

from app.db.in_memory import InMemoryStorage
from app.schemas.orders import CreateOrderInput
from app.services.geocoding import GeocodingError, NominatimGeocoder
from app.services.optimization import OptimizationService
from app.services.orders import OrdersService


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


if __name__ == "__main__":
    unittest.main()
