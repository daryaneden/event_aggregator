from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.exceptions import TicketNotFoundException
from app.application.use_cases.cancel_ticket import CancelTicketUseCase
from app.presentation.dependencies import get_cancel_ticket_use_case
from app.presentation.schemas.cancel_ticket_response import (
    CancelTicketResponse,
)


router = APIRouter(
    prefix="/api/tickets",
    tags=["cancel_ticket"],
)


@router.delete(
    "/{ticket_id}",
    response_model=CancelTicketResponse,
)
async def cancel_ticket(
    ticket_id: UUID,
    use_case: Annotated[
        CancelTicketUseCase,
        Depends(get_cancel_ticket_use_case),
    ],
):
    try:
        await use_case.execute(ticket_id)

    except TicketNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return CancelTicketResponse(success=True)