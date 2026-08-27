from pydantic import BaseModel, ConfigDict
from uuid import UUID

class PlaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    city: str
    address: str