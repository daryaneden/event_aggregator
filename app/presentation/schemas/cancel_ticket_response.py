from pydantic import BaseModel

class CancelTicketResponse(BaseModel):
    success: bool