import httpx
from datetime import datetime
from urllib.parse import urljoin
from uuid import UUID

from app.application.interfaces.event_provider import EventsProvider
from app.application.dtos.events_page import EventsPage
from app.application.dtos.register_ticket import RegisterTicketDTO
from app.domain.entities.event import Event
from app.domain.entities.place import Place
from app.infrastructure.event_provider.dtos.provider_event import ProviderEventDTO
from app.infrastructure.event_provider.dtos.provider_events_page import ProviderEventsPageDTO
from app.infrastructure.event_provider.dtos.provider_seats import ProviderSeatsDTO
from app.infrastructure.event_provider.dtos.provider_register_ticket import ProviderRegisterTicketDTO


class EventsProviderClient(EventsProvider):

    def __init__(self, client: httpx.AsyncClient, base_url: str):

        print(">>> EVENTS PROVIDER RECEIVED:", repr(client))
        print(">>> EVENTS PROVIDER TYPE:", type(client)) 

        self.client = client
        self.base_url = base_url


    async def get_events_page(self, changed_at: datetime, url: str | None = None) -> EventsPage:

        if url is None:
            url = urljoin(
        str(self.client.base_url),
        f"/api/events/?changed_at={changed_at.strftime('%Y-%m-%d')}"
)

        print(">>> REQUEST URL:", repr(url))
        print(">>> BASE URL:", repr(self.client.base_url))


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

    async def get_available_seats(
    self,
    event_id: UUID,
) -> list[str] | None:
        url = f"/api/events/{event_id}/seats/"

        response = await self.client.get(url)

        if response.status_code == 404:
            return None

        response.raise_for_status()

        dto = ProviderSeatsDTO.model_validate(response.json())

        return dto.seats

    async def register_ticket(
    self,
    data: RegisterTicketDTO,
) -> UUID:

        response = await self.client.post(
            f"/api/events/{data.event_id}/register/",
            json=ProviderRegisterTicketDTO(
                first_name=data.first_name,
                last_name=data.last_name,
                seat=data.seat,
                email=data.email,
            ).model_dump(),
        )

        response.raise_for_status()

        response_data = response.json()

        return UUID(response_data["ticket_id"])