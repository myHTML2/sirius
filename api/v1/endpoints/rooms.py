from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.room_service import get_all_rooms, create_room
from app.db.schemas.room import RoomCreate, RoomRead

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/", response_model=list[RoomRead])
def read_rooms(db: Session = Depends(get_db)):
    rooms = get_all_rooms(db)
    return rooms

@router.post("/", response_model=RoomRead)
def create_new_room(room_in: RoomCreate, db: Session = Depends(get_db)):
    room = create_room(db, room_data=room_in.model_dump())
    return room
  
