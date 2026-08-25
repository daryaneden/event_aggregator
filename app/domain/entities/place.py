from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Place:
    id: UUID
    name: str
    city: str
    address: str
    seats_pattern: str