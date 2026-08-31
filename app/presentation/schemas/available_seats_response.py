from pydantic import BaseModel
from uuid import UUID

class AvailableSeatsResponse(BaseModel):
    event_id: UUID
    available_seats: list[str]