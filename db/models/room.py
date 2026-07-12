from sqlalchemy import Column, Integer, String, JSON
from app.db.schemas.base_class import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    equipment = Column(JSON, nullable=False, default=[])
