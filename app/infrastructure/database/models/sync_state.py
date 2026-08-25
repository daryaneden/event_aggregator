from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class SyncStateModel(Base):
    __tablename__ = "sync_state"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_changed_at: Mapped[datetime|None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_sync_time: Mapped[datetime|None]
    sync_status: Mapped[str] = mapped_column(nullable=True)