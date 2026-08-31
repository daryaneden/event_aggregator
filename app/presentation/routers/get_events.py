from fastapi import APIRouter, Depends
from typing import Annotated

from app.presentation.schemas.get_events_request import GetEventsRequest
from app.presentation.dependencies import get_get_events_use_case, get_event_response_mapper
from app.application.use_cases.get_events import GetEventsUseCase
from app.presentation.mappers.event_response_mapper import EventResponseMapper

router = APIRouter(prefix="/api/events", tags=["get_events"])

@router.get('')
async def get_events(use_case: Annotated[GetEventsUseCase, Depends(get_get_events_use_case)],
                     mapper: Annotated[EventResponseMapper, Depends(get_event_response_mapper)],
                     request: Annotated[GetEventsRequest, Depends()]):

    events, total = await use_case.execute(
        date_from=request.date_from,
        page=request.page,
        page_size=request.page_size,
    )

    return mapper.to_list_response(
        events=events,
        total=total,
        page=request.page,
        page_size=request.page_size,
    )