"""Users models"""
from fastapi_users.db import SQLAlchemyBaseUserTable

from test_app.core.db import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    """_summary_

    Args:
        SQLAlchemyBaseUserTable (_type_): _description_
        Base (_type_): _description_
    """
