from uuid import UUID

from app.application.exceptions import EventNotFoundException
from app.application.interfaces.event_provider import EventsProvider
from app.application.interfaces.seats_cache_port import SeatsCachePort


class GetAvailableSeatsUseCase:

    def __init__(self, provider: EventsProvider,
        cache: SeatsCachePort):

        self.provider = provider
        self.cache = cache

    async def execute(self, event_id: UUID) -> list[str]:
        seats = self.cache.get(event_id)

        if seats is not None:
            return seats

        seats = await self.provider.get_available_seats(event_id)

        if seats is None:
            raise EventNotFoundException(event_id)

        self.cache.set(event_id, seats)

        return seats