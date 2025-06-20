"""CRUD operations for reservetion"""
from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.crud.base import CRUDBase
from test_app.models.reservation import Reservation

class CRUDReservation(CRUDBase):
    """_summary_

    Args:
        CRUDBase (_type_): _description_
    """

    async def get_reservations_at_the_same_time(self, from_reserve : datetime,
                                                to_reserve : datetime,
                                                meetingroom_id : int,
                                                session : AsyncSession) -> List[Reservation]:
        """_summary_

        Args:
            from_reserve (datetime): начальное время бронирования переговорки
            to_reserve (datetime): конечное время бронирования переговорки
            meetingroom_id (int): интересующая переговорка
            session (AsyncSession): асинхронная сессия из Dependency Injection

        Returns:
            List[Reservation]: _description_
        """

        return []

reservation_crud = CRUDReservation(Reservation)
