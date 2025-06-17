from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.core.db import get_async_session
from test_app.crud.meeting_room import meeting_room_crud
from test_app.schemas.meeting_room import (MeetingRoomCreate,
                                           MeetingRoomDB, MeetingRoomUpdate)
from test_app.api.validators import check_name_duplicate

router = APIRouter()


@router.post('/',response_model=MeetingRoomDB,response_model_exclude_none=True)
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate, session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(meeting_room.name,session)
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room

@router.get('/',response_model=list[MeetingRoomDB],response_model_exclude_none=True)
async def get_all_meeting_rooms(session: AsyncSession = Depends(get_async_session)):
    rooms = await meeting_room_crud.get_multi(session)
    return rooms

@router.patch('/{meeting_room_id}',response_model=MeetingRoomUpdate,response_model_exclude_none=True)
async def partially_update_meeting_room(meeting_room_id : int, update_data : MeetingRoomUpdate,session : AsyncSession = Depends(get_async_session)):
    room = await meeting_room_crud.get(meeting_room_id,session)
    if room is None:
        raise HTTPException(status_code=404,
                            detail="Переговорка не найдена!")
    if update_data.name is not None:
        await check_name_duplicate(update_data.name,session)
    room = await meeting_room_crud.update(room,update_data,session)
    return room

@router.delete('/{meeting_room_id}',response_model=MeetingRoomDB,response_model_exclude_none=True)
async def remove_meeting_room(meeting_room_id : int, session : AsyncSession = Depends(get_async_session)):
    room = await meeting_room_crud.get(meeting_room_id,session)
    if room is None:
        raise HTTPException(status_code=404,
                            detail="Переговорка не найдена!")
    meeting_room = await meeting_room_crud.remove(room,session)
    return meeting_room
