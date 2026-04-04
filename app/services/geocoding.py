from __future__ import annotations

from abc import ABC, abstractmethod

import requests


class GeocodingError(Exception):
    pass


class GeocodeResult:
    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude


class GeocoderInterface(ABC):
    @abstractmethod
    def geocode_address(self, address: str, city: str, st: str) -> GeocodeResult:
        pass


class NominatimGeocoder(GeocoderInterface):
    BASE_URL = "https://nominatim.openstreetmap.org/search"
    TIMEOUT_SECONDS = 10
    USER_AGENT = "cs-capstone/1.0 (student project geocoder)"

    def __init__(self, session: requests.Session | None = None) -> None:
        self._session = session or requests.Session()

    def geocode_address(self, address: str, city: str, st: str) -> GeocodeResult:
        try:
            response = self._session.get(
                self.BASE_URL,
                params={
                    "street": address,
                    "city": city,
                    "state": st,
                    "countrycodes": "us",
                    "format": "geocodejson",
                    "limit": 1,
                    "accept-language": "en",
                },
                headers={"User-Agent": self.USER_AGENT},
                timeout=self.TIMEOUT_SECONDS,
            )
        except requests.RequestException as exc:
            raise GeocodingError("Unable to reach the geocoding service.") from exc

        if response.status_code != 200:
            raise GeocodingError("The geocoding service returned an unexpected response.")

        try:
            payload = response.json()
            features = payload["features"]
            coordinates = features[0]["geometry"]["coordinates"]
            longitude = float(coordinates[0])
            latitude = float(coordinates[1])
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise GeocodingError("The geocoding service could not find that address.") from exc

        return GeocodeResult(latitude=latitude, longitude=longitude)
