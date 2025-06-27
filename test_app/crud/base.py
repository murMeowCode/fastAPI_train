"""base class for all CRUD ops"""
from typing import Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from test_app.models.user import User

class CRUDBase:
    """_summary_
    """

    def __init__(self, model):
        """_summary_

        Args:
            model (_type_): _description_
        """
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        """_summary_

        Args:
            obj_id (int): _description_
            session (AsyncSession): _description_

        Returns:
            _type_: _description_
        """
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """_summary_

        Args:
            session (AsyncSession): _description_

        Returns:
            _type_: _description_
        """
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user : Optional[User] = None
    ):
        """_summary_

        Args:
            obj_in (_type_): _description_
            session (AsyncSession): _description_

        Returns:
            _type_: _description_
        """
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        """_summary_

        Args:
            db_obj (_type_): _description_
            obj_in (_type_): _description_
            session (AsyncSession): _description_

        Returns:
            _type_: _description_
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        """_summary_

        Args:
            db_obj (_type_): _description_
            session (AsyncSession): _description_

        Returns:
            _type_: _description_
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj
