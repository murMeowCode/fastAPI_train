"""room_model"""
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from test_app.core.db import Base


class MeetingRoom(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    reservations = relationship('Reservation',cascade='delete')
