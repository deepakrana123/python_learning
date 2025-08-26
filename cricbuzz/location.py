from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Location:
    lat: float
    lon: float
    accuracy: float
    timestamp: datetime


@dataclass(frozen=True)
class Device:
    device_id: str
    user_id: str
    last_location: Location | None
    online: bool | False


class ILocationStream:
    def start_stream(self, device_id: str, location_iterator):
        """Start consuming a stream of locations from device via gRPC"""
        pass

    def handle_disconnect(self, device_id: str):
        """Called when device stream drops"""
        pass


class ILocationStore:
    def save_location(self, device_id: str, loc: Location):
        pass

    def get_last_location(self, device_id: str):
        pass

    def get_near_by_query(self, lat: str, lon: str):
        pass


import heapq
from math import radians, sin, cos, sqrt, atan2


class NearbyHeap:
    def __init__(self):
        self.locations = []

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371000
        d_lat = radians(lat2 - lat1)
        d_lon = radians(lon2 - lon1)
        a = (
            sin(d_lat / 2) ** 2
            + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
        )
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def add(self, user_id, lat, lon, ref_lat, ref_lon):
        dist = self.haversine(lat, lon, ref_lat, ref_lon)
        heapq.heappush(self.locations, (dist, user_id))

    def get_within_radius(self, radius_m):
        result = []
        while self.locations and self.locations[0][0] <= radius_m:
            dist, user_id = heapq.heappop(self.locations)
            result.append(user_id)
        return result


class IEventPublisher:
    def publish_location_update(self, device_id: str, loc: Location):
        None


class IClientNotifier:
    def push_location(self, subscriber_id: str, device_id: str, loc: Location):
        None


class LocationIngestService:
    def __init__(self, store: ILocationStore, publisher: IEventPublisher):
        self.store = store
        self.publisher = publisher

    def ingest(self, device_id: str, location_iterator):
        try:
            for loc in location_iterator:
                self.store.save_location(device_id, loc)
                self.publisher.publish_location_update(device_id, loc)
        except ConnectionError:
            self.handle_disconnect(device_id)

    def handle_disconnect(self, device_id: str):
        last_loc = self.store.get_last_location(device_id)


class LocationFanOutService:
    def __init__(self, store: ILocationStore, notifier: IClientNotifier):
        self.store = store
        self.notifier = notifier

    def on_location_update(self, device_id: str, loc: Location):
        subscribers = self._get_subscribers_for_device(device_id)
        for sid in subscribers:
            self.notifier.push_location(sid, device_id, loc)

    def _get_subscribers_for_device(self, device_id: str) -> list[str]:
        return []
