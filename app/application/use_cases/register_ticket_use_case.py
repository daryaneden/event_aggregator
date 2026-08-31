from uuid import UUID

from app.application.dtos.register_ticket import RegisterTicketDTO
from app.application.interfaces.event_provider import EventsProvider

class RegisterTicketUseCase:

    def __init__(self, provider: EventsProvider):
        self.provider = provider

    async def execute(self, data: RegisterTicketDTO) -> UUID:
        return await self.provider.register_ticket(data)