""""endpoints for reservations"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.models import User
from test_app.schemas.reservation import ReservationDB, ReservationCreate, ReservationUpdate
from test_app.core.db import get_async_session
from test_app.core.user import current_user
from test_app.crud.reservation import reservation_crud
from test_app.api.validators import (
    check_meeting_room_exists, check_reservation_interceptions, check_reservation_before_edit)
router = APIRouter()

@router.post('/',response_model=ReservationDB,response_model_exclude_none=True)
async def create_reservation(reservation : ReservationCreate,
                             session : AsyncSession = Depends(get_async_session),
                             user : User = Depends(current_user)):
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
        reservation,session,user)

    return new_reservation

@router.get('/',response_model=List[ReservationDB])
async def get_all_reservations(session : AsyncSession = Depends(get_async_session)):
    """_summary_

    Args:
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).

    Returns:
        _type_: _description_
    """
    reservations = reservation_crud.get_multi(session)
    return await reservations

@router.delete('/{reservation_id}',response_model=ReservationDB)
async def delete_reservation(reservation_id : int,
                             session : AsyncSession = Depends(get_async_session)):
    """_summary_

    Args:
        reservation_id (int): _description_
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).

    Returns:
        _type_: _description_
    """
    reservation = await check_reservation_before_edit(
        reservation_id=reservation_id,
        session=session
    )
    reservation = reservation_crud.remove(reservation,session)
    return reservation

@router.patch('/{reservation_id}',response_model=ReservationDB)
async def update_reservation(reservation_id : int, obj_in : ReservationUpdate,
                             session : AsyncSession = Depends(get_async_session)):
    """_summary_

    Args:
        reservation_id (int): _description_
        obj_in (ReservationUpdate): _description_
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).

    Returns:
        _type_: _description_
    """
    reservation = await check_reservation_before_edit(reservation_id,session)
    await check_reservation_interceptions(**obj_in.model_dump,
                                          reservation_id=reservation_id,
                                          meetingroom_id = reservation.meetingroom_id,
                                          session=session)
    reservation = reservation_crud.update(db_obj=reservation,obj_in=obj_in,session=session)
    return reservation
