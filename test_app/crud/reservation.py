"""CRUD operations for reservetion"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.crud.base import CRUDBase
from test_app.models.reservation import Reservation

class CRUDReservation(CRUDBase):
    """_summary_

    Args:
        CRUDBase (_type_): _description_
    """

    async def get_reservations_at_the_same_time(self,*, from_reserve : datetime,
                                                to_reserve : datetime,
                                                meetingroom_id : int,
                                                reservation_id : Optional[int] = None,
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
        select_smt = select(Reservation).where(
                Reservation.meetingroom_id == meetingroom_id,
                and_(
                    from_reserve <= Reservation.to_reserve,
                    to_reserve >= Reservation.from_reserve
                ))
        if reservation_id is not None:
            select_smt = select_smt.where(
                Reservation.id != reservation_id
            )
        rooms = await session.execute(select_smt)
        rooms = rooms.scalars.all()
        return rooms

reservation_crud = CRUDReservation(Reservation)
