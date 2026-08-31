from pydantic import BaseModel

class ProviderSeatsDTO(BaseModel):
    seats: list[str]