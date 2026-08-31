from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.use_cases.get_available_seats import (
    GetAvailableSeatsUseCase,
)
from app.application.exceptions import EventNotFoundException
from app.presentation.dependencies import get_available_seats_use_case
from app.presentation.schemas.available_seats_response import AvailableSeatsResponse


router = APIRouter(
    prefix="/api/events",
    tags=["get_seats"],
)


@router.get(
    "/{event_id}/seats",
    response_model=AvailableSeatsResponse,
)
async def get_available_seats(
    event_id: UUID,
    use_case: Annotated[
        GetAvailableSeatsUseCase,
        Depends(get_available_seats_use_case),
    ],
):
    try:
        seats = await use_case.execute(event_id)

    except EventNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return AvailableSeatsResponse(seats=seats)