from dataclasses import dataclass
from uuid import UUID


@dataclass
class OutboxMessageDto:
    event_type: str
    payload: dict

@dataclass
class PendingOutboxMessage:
    id: UUID
    event_type: str
    payload: dict