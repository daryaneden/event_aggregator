from dataclasses import dataclass


@dataclass(frozen=True)
class BusinessMetricsDto:
    tickets_count: int
    cancelled_tickets_count: int
    events_count: int