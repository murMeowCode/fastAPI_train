from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.core.db import get_async_session
from test_app.crud.meeting_room import create_meeting_room, get_meeting_room_by_id,get_room_id_by_name,read_all_rooms_from_db, update_meeting_room,delete_meeting_room
from test_app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate

router = APIRouter(prefix='/meeting_rooms')


@router.post('/',response_model=MeetingRoomDB,response_model_exclude_none=True)
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate, session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(meeting_room.name,session)
    new_room = await create_meeting_room(meeting_room, session)
    return new_room

@router.get('/',response_model=list[MeetingRoomDB],response_model_exclude_none=True)
async def get_all_meeting_rooms(session: AsyncSession = Depends(get_async_session)):
    rooms = await read_all_rooms_from_db(session)
    return rooms

@router.patch('/{meeting_room_id}',response_model=MeetingRoomUpdate,response_model_exclude_none=True)
async def partially_update_meeting_room(meeting_room_id : int, update_data : MeetingRoomUpdate,session : AsyncSession = Depends(get_async_session)):
    room = await get_meeting_room_by_id(meeting_room_id,session)
    if room is None:
        raise HTTPException(status_code=404,
                            detail="Переговорка не найдена!")
    if update_data.name is not None:
        await check_name_duplicate(update_data.name,session)
    room = await update_meeting_room(room,update_data,session)
    return room

@router.delete('/{meeting_room_id}',response_model=MeetingRoomDB,response_model_exclude_none=True)
async def remove_meeting_room(meeting_room_id : int, session : AsyncSession = Depends(get_async_session)):
    room = await get_meeting_room_by_id(meeting_room_id,session)
    if room is None:
        raise HTTPException(status_code=404,
                            detail="Переговорка не найдена!")
    meeting_room = await delete_meeting_room(room,session)
    return meeting_room    

async def check_name_duplicate(room_name : str, session : AsyncSession) -> None:
    room_id = await get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )
