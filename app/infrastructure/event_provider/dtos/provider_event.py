from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.infrastructure.event_provider.dtos.provider_place import ProviderPlaceDTO


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