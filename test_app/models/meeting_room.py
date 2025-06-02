"""room_model"""
from sqlalchemy import Column, String, Text

# Импортируем базовый класс для моделей.
from test_app.core.db import Base


class MeetingRoom(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
