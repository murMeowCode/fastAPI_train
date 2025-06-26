"""schemas for user"""
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """_summary_

    Args:
        schemas (_type_): _description_
    """

class UserCreate(schemas.BaseUserCreate):
    """_summary_

    Args:
        schemas (_type_): _description_
    """

class UserUpdate(schemas.BaseUserUpdate):
    """_summary_

    Args:
        schemas (_type_): _description_
    """
