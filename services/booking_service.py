from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.db.models.booking import Booking, BookingStatus
from app.db.schemas.booking import BookingCreateSchema


def get_bookings_for_room(db: Session, *, room_id: int, date: str = None) -> List[Booking]:
    query = (
        db.query(Booking)
        .filter(Booking.room_id == room_id)
        .filter(Booking.status == BookingStatus.active)
    )
    
    if date:
        query = query.filter(Booking.start_time >= f"{date} 00:00:00")
        query = query.filter(Booking.end_time <= f"{date} 23:59:59")
    
    return query.all()


def is_booking_intersected(
    db: Session,
    *,
    new_start: datetime,
    new_end: datetime,
    room_id: int,
    ignore_id: int | None = None,
) -> bool:

    existing_bookings = get_bookings_for_room(db, room_id=room_id)

    for b in existing_bookings:
        if b.id == ignore_id:
            continue

        if not (new_end < b.start_time or new_start > b.end_time):
            return True  # Пересечение найдено!
    return False
