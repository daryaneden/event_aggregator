from uuid import UUID

from pydantic import BaseModel


class ProviderSeatsDTO(BaseModel):
    event_id: UUID
    available_seats: list[str]