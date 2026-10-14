from datetime import datetime
from urllib.parse import urljoin
from uuid import UUID
import time

import httpx

from app.application.dtos.events_page import EventsPage
from app.application.dtos.register_ticket import RegisterTicketDTO
from app.application.interfaces.events_provider import EventsProvider
from app.domain.entities.event import Event
from app.domain.entities.place import Place
from app.infrastructure.event_provider.dtos.provider_event import ProviderEventDTO
from app.infrastructure.event_provider.dtos.provider_events_page import (
    ProviderEventsPageDTO,
)
from app.infrastructure.event_provider.dtos.provider_register_ticket import (
    ProviderRegisterTicketDTO,
)
from app.infrastructure.event_provider.dtos.provider_seats import ProviderSeatsDTO

from app.infrastructure.metrics import (
    events_provider_requests_total,
    events_provider_request_duration_seconds,
)

class EventsProviderClient(EventsProvider):

    def __init__(self, client: httpx.AsyncClient, base_url: str):

        self.client = client
        self.base_url = base_url

    async def get_events_page(self, changed_at: datetime, url: str | None = None) -> EventsPage:

        if url is None:
            url = urljoin(str(self.client.base_url),
        f'/api/events/?changed_at={changed_at.strftime('%Y-%m-%d')}')

        response = await self._request(method="GET",
                                       url=url,
                                       endpoint="/events")
        response.raise_for_status()

        dto = ProviderEventsPageDTO.model_validate(response.json())

        return self._to_page(dto)

    def _to_page(self, dto: ProviderEventsPageDTO) -> EventsPage:

        events = [self._to_domain(event) for event in dto.results]

        return EventsPage(events=events, next_url=dto.next)

    def _to_domain(self, dto: ProviderEventDTO) -> Event:

        return Event(id=dto.id,
            name=dto.name,
            place=Place(
                id=dto.place.id,
                name=dto.place.name,
                city=dto.place.city,
                address=dto.place.address,
                seats_pattern=dto.place.seats_pattern),
            event_time=dto.event_time,
            registration_deadline=dto.registration_deadline,
            status=dto.status,
            number_of_visitors=dto.number_of_visitors,
            changed_at=dto.changed_at,
            created_at=dto.created_at,
            status_changed_at=dto.status_changed_at)

    async def get_available_seats(self, event_id: UUID) -> list[str] | None:
        url = f'/api/events/{event_id}/seats/'

        response = await self._request(method="GET",
                                       url=url,
                                       endpoint="/seats")

        if response.status_code == 404:
            return None

        response.raise_for_status()

        dto = ProviderSeatsDTO.model_validate(response.json())

        return dto.seats

    async def register_ticket(self, data: RegisterTicketDTO) -> UUID:

        response = await self._request(method="POST",
                                       url=f"/api/events/{data.event_id}/register/",
                                       endpoint="/registration",
                                       json=ProviderRegisterTicketDTO(first_name=data.first_name,
                                                                      last_name=data.last_name,
                                                                      seat=data.seat,
                                                                      email=data.email).model_dump())
        response.raise_for_status()

        response_data = response.json()

        return UUID(response_data['ticket_id'])

    async def cancel_ticket(self, event_id: UUID, ticket_id: UUID) -> bool:

        response = await self._request(method="DELETE",
                                       url=f"/api/events/{event_id}/unregister/",
                                       endpoint="/registration",
                                       json={"ticket_id": str(ticket_id)})

        response.raise_for_status()

        return True

    async def _request(self, method: str, url: str, endpoint: str, **kwargs) -> httpx.Response:
        start_time = time.monotonic()
        status = 'error'

        try:
            response = await self.client.request(method=method,
                                                 url=url,
                                                 **kwargs)

            status = str(response.status_code)
            return response

        finally:
            duration = time.monotonic() - start_time

            events_provider_requests_total.labels(endpoint=endpoint,
                                                  status=status).inc()

            events_provider_request_duration_seconds.labels(endpoint=endpoint).observe(duration)

    