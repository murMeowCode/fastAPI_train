# Импортируем sessionmaker из файла с настройками БД.
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.models.meeting_room import MeetingRoom
from test_app.schemas.meeting_room import MeetingRoomCreate


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
