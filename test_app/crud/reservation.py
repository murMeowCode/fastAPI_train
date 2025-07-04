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

    async def get_reservations_at_the_same_time(self,*, from_reserve : datetime, #pylint: disable=R0913
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
        rooms = rooms.scalars().all()
        return rooms

    async def get_future_reservations_for_room(self, room_id : int,
                                                session : AsyncSession)-> List[Reservation]:
        """_summary_

        Args:
            room_id (int): _description_
            session (AsyncSession): _description_

        Returns:
            _type_: _description_
        """
        future_reservations = await session.execute(
            select(Reservation).where(Reservation.meetingroom_id == room_id,
                                      and_(Reservation.to_reserve > datetime.now()))
        )
        future_reservations = future_reservations.scalars().all()
        return future_reservations

    async def get_by_user(self,session : AsyncSession,user_id : int) -> List[Reservation]:
        """_summary_

        Args:
            session (AsyncSession): _description_
            user_id (int): _description_

        Returns:
            List[Reservation]: _description_
        """
        reservations = await session.execute(
            select(Reservation).where(Reservation.user_id == user_id)
        )
        reservations = reservations.scalars().all()
        return reservations

reservation_crud = CRUDReservation(Reservation)
