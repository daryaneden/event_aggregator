from fastapi import APIRouter, Depends
from typing import Annotated

from app.presentation.schemas.create_ticket_request import CreateTicketRequest
from app.presentation.schemas.ticket_response import TicketResponse
from app.application.dtos.register_ticket import RegisterTicketDTO
from app.application.use_cases.create_ticket import CreateTicketUseCase
from app.presentation.dependencies import get_create_ticket_use_case

router = APIRouter(
    prefix="/api/tickets",
    tags=["tickets"],
)

@router.post(
    "",
    response_model=TicketResponse,
    status_code=201,
)
async def register_ticket(
    request: CreateTicketRequest,
    use_case: Annotated[
        CreateTicketUseCase,
        Depends(get_create_ticket_use_case),
    ],
):
    data = RegisterTicketDTO(
        event_id=request.event_id,
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        seat=request.seat,
    )

    ticket_id = await use_case.execute(data)

    return TicketResponse(ticket_id=ticket_id)