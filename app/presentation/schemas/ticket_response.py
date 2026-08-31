from uuid import UUID 
from pydantic import BaseModel, EmailStr 

class TicketResponse(BaseModel): 
    ticket_id: UUID