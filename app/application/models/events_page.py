from dataclasses import dataclass

from app.domain.entities.event import Event


@dataclass
class EventsPage:
    events: list[Event]
    next_url: str | None