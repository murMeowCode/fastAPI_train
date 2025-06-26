"""module for param validations"""
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from test_app.crud.meeting_room import meeting_room_crud
from test_app.crud.reservation import reservation_crud
from test_app.models.meeting_room import MeetingRoom

async def check_name_duplicate(room_name : str, session : AsyncSession) -> None:
    """_summary_

    Args:
        room_name (str): _description_
        session (AsyncSession): _description_

    Raises:
        HTTPException: _description_
    """
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )

async def check_meeting_room_exists(
        meeting_room_id: int,
        session: AsyncSession,
) -> MeetingRoom:
    """_summary_

    Args:
        meeting_room_id (int): _description_
        session (AsyncSession): _description_

    Raises:
        HTTPException: _description_

    Returns:
        MeetingRoom: _description_
    """
    meeting_room = await meeting_room_crud.get(meeting_room_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return meeting_room

async def check_reservation_interceptions(**kwargs) -> None:
    """_summary_
    """
    reservations = await reservation_crud.get_reservations_at_the_same_time( #pylint: disable=E1125
        **kwargs
    )
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=str(reservations)
        )

async def check_reservation_before_edit(reservation_id : int,
                                         session : AsyncSession):
    """_summary_

    Args:
        reservation_id (int): _description_
        session (AsyncSession): _description_

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    reservation = reservation_crud.get(reservation_id,session)
    if not reservation:
        raise HTTPException(
            status_code=404,
            detail='Бронь не найдена!'
        )
    return reservation
