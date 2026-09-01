from urllib.parse import urlencode

from app.domain.entities.event import Event
from app.presentation.schemas.event_list_response import EventListResponse
from app.presentation.schemas.event_response import EventResponse
from app.presentation.schemas.place_response import PlaceResponse


class EventResponseMapper:

    def to_response(self, event: Event) -> EventResponse:
        return EventResponse(id=event.id,
            name=event.name,
            place=PlaceResponse(id=event.place.id,
                                name=event.place.name,
                                city=event.place.city,
                                address=event.place.address,
                                seats_pattern=event.place.seats_pattern),
            event_time=event.event_time,
            registration_deadline=event.registration_deadline,
            status=event.status,
            number_of_visitors=event.number_of_visitors)

    def to_list_response(self, events: list[Event],
                         total: int,
                         page: int,
                         page_size: int) -> EventListResponse:

        next_url = None
        previous_url = None

        if page * page_size < total:
            next_url = self.build_page_url(page=page + 1,
                                           page_size=page_size)

        if page > 1:
            previous_url = self.build_page_url(page=page - 1,
                                               page_size=page_size)

        return EventListResponse(count=total,
                                 next=next_url,
                                 previous=previous_url,
                                 results=[self.to_response(event) for event in events])

    def build_page_url(self, page: int, page_size: int) -> str:
        query = urlencode({'page': page,
                           'page_size': page_size})

        return f'/api/events?{query}'