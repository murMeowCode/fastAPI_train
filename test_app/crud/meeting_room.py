# Импортируем sessionmaker из файла с настройками БД.
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.models.meeting_room import MeetingRoom
from test_app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


# Функция работает с асинхронной сессией, 
# поэтому ставим ключевое слово async.
# В функцию передаём схему MeetingRoomCreate.
async def create_meeting_room(
        new_room: MeetingRoomCreate, session: AsyncSession
) -> MeetingRoom:
    # Конвертируем объект MeetingRoomCreate в словарь.
    new_room_data = new_room.model_dump()

    db_room = MeetingRoom(**new_room_data)

    session.add(db_room)

    await session.commit()

    # Обновляем объект db_room: считываем данные из БД, чтобы получить его id.
    await session.refresh(db_room)
    # Возвращаем только что созданный объект класса MeetingRoom.
    return db_room

async def get_room_id_by_name(room_name : str,
                              session: AsyncSession) -> Optional[int]:
    """_summary_

    Args:
        room_name (str): _description_

    Returns:
        Optional[int]: _description_
    """
    db_room_id = await session.execute(
        select(MeetingRoom.id).where(MeetingRoom.name == room_name)
    )
    db_room_id = db_room_id.scalars().first()
    return db_room_id

async def read_all_rooms_from_db(
        session: AsyncSession,
) -> list[MeetingRoom]:
    db_rooms = await session.execute(select(MeetingRoom))
    return db_rooms.scalars().all()

async def get_meeting_room_by_id(room_id : int,
                                 session : AsyncSession) -> Optional[MeetingRoom]:
    db_room = await session.execute(
        select(MeetingRoom).where(MeetingRoom.id == room_id)
    )
    return db_room.scalars().first()

async def update_meeting_room(db_room : MeetingRoom, room_in : MeetingRoomUpdate,
                              session : AsyncSession) -> MeetingRoom:
    obj_data = jsonable_encoder(db_room)
    update_data = room_in.model_dump(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_room,field,update_data[field])

    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)

    return db_room

async def delete_meeting_room(db_room : MeetingRoom,
                              session : AsyncSession) -> MeetingRoom:
    await session.delete(db_room)
    await session.commit()
    return db_room