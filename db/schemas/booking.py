from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class BookingBase(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class BookingRead(BookingBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
