from uuid import UUID

from app.application.interfaces.seats_cache_port import SeatsCachePort
from app.infrastructure.metrics import cache_hits_total, cache_misses_total


class MetricsSeatsCache(SeatsCachePort):
    def __init__(self, cache: SeatsCachePort):
        self._cache = cache

    def get(self, event_id: UUID) -> list[str] | None:
        seats = self._cache.get(event_id)

        if seats is None:
            cache_misses_total.inc()
        else:
            cache_hits_total.inc()

        return seats

    def set(self, event_id: UUID, seats: list[str]) -> None:
        self._cache.set(event_id, seats)