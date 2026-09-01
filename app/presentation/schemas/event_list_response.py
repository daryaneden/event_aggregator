from pydantic import BaseModel

from app.presentation.schemas.event_response import EventResponse

class EventListResponse(BaseModel):
    count: int
    next: str | None
    previous: str | None
    results: list[EventResponse]