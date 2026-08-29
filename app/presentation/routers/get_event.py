from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from uuid import UUID

from app.presentation.schemas.event_response import EventResponse
from app.application.exceptions import EventNotFoundException
from app.presentation.dependencies import get_get_event_use_case, get_event_response_mapper
from app.application.use_cases.get_event import GetEventUseCase
from app.presentation.mappers.event_response_mapper import EventResponseMapper

router = APIRouter(prefix="/api/events", tags=["get_event"])

@router.get(
    "/{event_id}",
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
    try:

        event = await use_case.execute(event_id)

    except EventNotFoundException as e:
        raise HTTPException(status_code=404,
                            detail = e.detail)

    return mapper.to_response(event)