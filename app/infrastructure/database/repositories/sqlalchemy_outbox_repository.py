import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dtos.outbox_message import OutboxMessageDto
from app.application.interfaces.outbox_repository import OutboxRepository
from app.infrastructure.database.models.outbox_event import OutboxEventModel


class SqlAlchemyOutboxRepository(OutboxRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, message: OutboxMessageDto) -> None:
        outbox_event = OutboxEventModel(
            id=uuid.uuid4(),
            event_type=message.event_type,
            payload=message.payload,
            status="pending",
            created_at=datetime.now(UTC),
        )

        self.session.add(outbox_event)