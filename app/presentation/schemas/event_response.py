from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.presentation.schemas.place_response import PlaceResponse


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    place: PlaceResponse
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int