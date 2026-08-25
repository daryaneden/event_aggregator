from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SyncStatus(Enum, str):
    NEVER_RUN = "never_run"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class SyncState:
    last_sync_time: datetime | None
    last_changed_at: datetime | None
    sync_status: SyncStatus