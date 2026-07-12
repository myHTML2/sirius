from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.db.database import Base

class BookingStatus(PyEnum):
    active = "active"
    cancelled = "cancelled"
    completed = "completed"

class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.active, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
