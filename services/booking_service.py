from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.booking import Booking, BookingStatus

def get_bookings_for_room(db: Session, *, room_id: int, date: Optional[str] = None) -> List[Booking]:
    """Получает все активные бронирования комнаты."""
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
    ignore_id: Optional[int] = None,
) -> bool:

    existing_bookings = get_bookings_for_room(db, room_id=room_id)

    for b in existing_bookings:
        # Пропускаем текущее бронирование при редактировании
        if b.id == ignore_id:
            continue

        # Логика перекрытия интервалов
        # https://ru.stackoverflow.com/a/476835
        if not (new_end < b.start_time or new_start > b.end_time):
            return True  # Пересечение найдено!
    return False

def create_booking(
    db: Session,
    room_id: int,
    start_time: datetime,
    end_time: datetime,
    user_id: int | None = None, 
    ignore_id: int | None = None
):
    # Проверка пересечения интервалов
    if is_booking_intersected(db, new_start=start_time, new_end=end_time, room_id=room_id, ignore_id=ignore_id):
        raise ValueError("Время занято")

    booking = Booking(room_id=room_id, start_time=start_time, end_time=end_time, user_id=user_id)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
