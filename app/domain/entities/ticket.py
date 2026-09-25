from dataclasses import dataclass
from uuid import UUID


@dataclass
class Ticket:
    id: UUID
    event_id: UUID
    first_name: str
    last_name: str
    email: str
    seat: str