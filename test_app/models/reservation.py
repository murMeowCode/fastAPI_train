"""description of reservation models"""
from sqlalchemy import Column, DateTime, ForeignKey, Integer

from test_app.core.db import Base


class Reservation(Base):
    """_summary_

    Args:
        Base (_type_): Базовый класс модели бронирования
    """
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    # Столбец с внешним ключом: ссылка на таблицу meetingroom.
    meetingroom_id = Column(Integer, ForeignKey('meetingroom.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'
