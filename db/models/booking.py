import enum
from datetime import datetime
from sqlalchemy import Column, ForeignKey, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from app.db.schemas.base_class import Base


class BookingStatus(enum.Enum):
    active = "active"
    cancelled = "cancelled"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
    )
    room = relationship("Room")  # Связь для удобного доступа к комнате

    user_name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(BookingStatus), nullable=False, default=BookingStatus.active)
