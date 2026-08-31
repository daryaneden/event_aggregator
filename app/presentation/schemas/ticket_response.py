from uuid import UUID

from pydantic import BaseModel


class TicketResponse(BaseModel): 
    ticket_id: UUID