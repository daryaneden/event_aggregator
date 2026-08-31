from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ProviderPlaceDTO(BaseModel):
    id: UUID
    name: str
    city: str
    address: str
    seats_pattern: str
    changed_at: datetime
    created_at: datetime

class ProviderEventDTO(BaseModel):
    id: UUID
    name: str
    place: ProviderPlaceDTO
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int
    changed_at: datetime
    created_at: datetime
    status_changed_at: datetime

class ProviderEventsPageDTO(BaseModel):
    results: list[ProviderEventDTO]
    next: str | None

class ProviderSeatsDTO(BaseModel):
    seats: list[str]

class ProviderRegisterTicketDTO(BaseModel): 
    first_name: str 
    last_name: str 
    seat: str 
    email: str