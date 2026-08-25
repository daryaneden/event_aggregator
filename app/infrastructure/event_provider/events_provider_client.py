import httpx
from datetime import datetime

from app.application.interfaces.event_provider import EventsProvider
from app.application.models.events_page import EventsPage
from app.domain.entities.event import Event
from app.domain.entities.place import Place
from app.infrastructure.event_provider.dtos import ProviderEventDTO, ProviderEventsPageDTO


class EventsProviderClient(EventsProvider):

    def __init__(self, client: httpx.AsyncClient):
        self.client = client


    async def get_events_page(self, changed_at: datetime, url: str | None = None) -> EventsPage:

        if url is None:
            url = (
                f"/api/events/"
                f"?changed_at={changed_at}")

        response = await self.client.get(url)
        response.raise_for_status()

        dto = ProviderEventsPageDTO.model_validate(response.json())

        return self._to_page(dto)

    def _to_page(self, dto: ProviderEventsPageDTO) -> EventsPage:

        events = [self._to_domain(event) for event in dto.results]

        return EventsPage(
            events=events,
            next_url=dto.next,
        )

    def _to_domain(self, dto: ProviderEventDTO) -> Event:

        return Event(
            id=dto.id,
            name=dto.name,
            place=Place(
                id=dto.place.id,
                name=dto.place.name,
                city=dto.place.city,
                address=dto.place.address,
                seats_pattern=dto.place.seats_pattern,
            ),
            event_time=dto.event_time,
            registration_deadline=dto.registration_deadline,
            status=dto.status,
            number_of_visitors=dto.number_of_visitors,
            changed_at=dto.changed_at,
            created_at=dto.created_at,
            status_changed_at=dto.status_changed_at
        )