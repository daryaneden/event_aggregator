from uuid import UUID

from pydantic import BaseModel, EmailStr

class CreateTicketRequest(BaseModel): 
    event_id: UUID 
    first_name: str 
    last_name: str 
    email: EmailStr 
    seat: str 
