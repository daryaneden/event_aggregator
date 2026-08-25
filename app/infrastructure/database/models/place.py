import uuid
from app.infrastructure.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class PlaceModel(Base):
    __tablename__ = "places"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    seats_pattern: Mapped[str] = mapped_column()