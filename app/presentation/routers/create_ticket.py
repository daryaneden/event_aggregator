from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException

from app.application.dtos.register_ticket import RegisterTicketDTO
from app.application.exceptions import TicketIdempotencyConflict
from app.application.use_cases.create_ticket import CreateTicketUseCase
from app.presentation.dependencies import get_create_ticket_use_case
from app.presentation.schemas.create_ticket_request import CreateTicketRequest
from app.presentation.schemas.ticket_response import TicketResponse

router = APIRouter(prefix="/api/tickets", tags=["tickets"])

@router.post("", response_model=TicketResponse, status_code=201)
async def register_ticket(request: CreateTicketRequest,
                          use_case: Annotated[CreateTicketUseCase, Depends(get_create_ticket_use_case)],
                          idempotency_key: str | None = Header(default=None)):
        
    data = RegisterTicketDTO(event_id=request.event_id,
                            first_name=request.first_name,
                            last_name=request.last_name,
                            email=request.email,
                            seat=request.seat,
                            idempotency_key=idempotency_key)
    try: 
        ticket_id = await use_case.execute(data)

    except TicketIdempotencyConflict:
            raise HTTPException(status_code=409)

    return TicketResponse(ticket_id=ticket_id)