""""endpoints for reservations"""
from fastapi import APIRouter, Depends
from test_app.schemas.reservation import ReservationDB, ReservationCreate
from test_app.core.db import get_async_session
from test_app.crud.reservation import reservation_crud
from test_app.api.validators import (
    check_meeting_room_exists, check_reservation_interceptions)
router = APIRouter()

@router.post('/',response_model=ReservationDB,response_model_exclude_none=True)
async def create_reservation(reservation : ReservationCreate,
                             session = Depends(get_async_session)):
    """_summary_

    Args:
        reservation (ReservationCreate): данные пользователя о бронировании
        session (_type_, optional): асинхронная сессия для БД.

    Returns:
        ReservationDB: запись о созданной брони из БД
    """
    await check_meeting_room_exists(reservation.meetingroom_id, session)
    await check_reservation_interceptions(**reservation.model_dump(),
                                          session=session)
    new_reservation = await reservation_crud.create(
        reservation,session)

    return new_reservation
