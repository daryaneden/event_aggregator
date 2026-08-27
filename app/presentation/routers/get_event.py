from fastapi import APIRouter, Depends
from typing import Annotated
from uuid import UUID

from app.presentation.schemas.event_response import EventResponse
from app.presentation.schemas.get_events_request import GetEventsRequest
from app.presentation.dependencies import get_get_event_use_case, get_event_response_mapper
from app.application.use_cases.get_event import GetEventUseCase
from app.presentation.mappers.event_response_mapper import EventResponseMapper

router = APIRouter(prefix="/api/event", tags=["get_event"])

@router.get(
    "/api/events/{event_id}",
    response_model=EventResponse,
)
async def get_event(
    event_id: UUID,
    use_case: Annotated[
        GetEventUseCase,
        Depends(get_get_event_use_case),
    ],
    mapper: Annotated[
        EventResponseMapper,
        Depends(get_event_response_mapper),
    ],
):
    event = await use_case.execute(event_id)

    return mapper.to_response(event)