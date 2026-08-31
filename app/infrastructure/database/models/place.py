import uuid
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.database import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.event import EventModel

class PlaceModel(Base):
    __tablename__ = "places"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    seats_pattern: Mapped[str] = mapped_column()
    events: Mapped[list["EventModel"]] = relationship("EventModel", back_populates="place")