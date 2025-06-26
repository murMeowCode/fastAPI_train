"""CRUD for meetingroom"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from test_app.crud.base import CRUDBase
from test_app.models.meeting_room import MeetingRoom

class CRUDMeetingRoom(CRUDBase):
    """_summary_

    Args:
        CRUDBase (_type_): _description_
    """

    async def get_room_id_by_name(
            self,
            room_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """_summary_

        Args:
            room_name (str): _description_
            session (AsyncSession): _description_

        Returns:
            Optional[int]: _description_
        """
        db_room_id = await session.execute(
            select(MeetingRoom.id).where(
                MeetingRoom.name == room_name
            )
        )
        db_room_id = db_room_id.scalars().first()
        return db_room_id

meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
