from pydantic import BaseModel


class ProviderRegisterTicketDTO(BaseModel): 
    first_name: str 
    last_name: str 
    seat: str 
    email: str