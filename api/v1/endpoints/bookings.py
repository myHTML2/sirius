from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.core.database import get_db
from app.db.schemas.booking import BookingCreate, BookingRead, BookingUpdate
from app.services.booking_service import get_bookings_for_room, is_booking_intersected

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(booking_in: BookingCreate, db: Session = Depends(get_db)):
    if is_booking_intersected(
        db,
        new_start=booking_in.start_time,
        new_end=booking_in.end_time,
        room_id=booking_in.room_id
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Выбранное время уже занято."
        )
    
    booking = Booking(**booking_in.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@router.get("/room/{room_id}", response_model=List[BookingRead])
def read_bookings_for_room(room_id: int, date: str = None, db: Session = Depends(get_db)):
    bookings = get_bookings_for_room(db, room_id=room_id, date=date)
    return bookings


