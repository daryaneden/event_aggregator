from pydantic import BaseModel

class AvailableSeatsResponse(BaseModel):
    seats: list[str]