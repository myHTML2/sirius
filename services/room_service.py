from typing import List
from sqlalchemy.orm import Session
from app.db.models.room import Room

def get_all_rooms(db: Session) -> List[Room]:
    return db.query(Room).all()

def create_room(db: Session, room_data: dict) -> Room:
    new_room = Room(**room_data)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room
  
