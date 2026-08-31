from dataclasses import dataclass
from uuid import UUID


@dataclass
class Place:
    id: UUID
    name: str
    city: str
    address: str
    seats_pattern: str