from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from app.domain.entities.place import Place

@dataclass
class Event:

    id: UUID
    name: str
    place: Place
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int
    changed_at: datetime
    created_at: datetime
    status_changed_at: datetime 