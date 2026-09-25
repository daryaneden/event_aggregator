from dataclasses import dataclass

@dataclass
class OutboxMessageDto:
    event_type: str
    payload: dict