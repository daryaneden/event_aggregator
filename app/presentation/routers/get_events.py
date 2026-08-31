from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.use_cases.get_events import GetEventsUseCase
from app.presentation.dependencies import (
    get_event_response_mapper,
    get_get_events_use_case,
)
from app.presentation.mappers.event_response_mapper import EventResponseMapper
from app.presentation.schemas.get_events_request import GetEventsRequest

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