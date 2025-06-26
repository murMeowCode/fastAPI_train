"""auth settings"""
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from test_app.core.config import Settings
from test_app.core.db import get_async_session
from test_app.models.user import User
from test_app.schemas.user import UserCreate

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """_summary_

    Args:
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).

    Yields:
        _type_: _description_
    """
    yield SQLAlchemyUserDatabase(session,User)

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')

def get_jwt_strategy() -> JWTStrategy:
    """_summary_

    Returns:
        JWTStrategy: _description_
    """
    return JWTStrategy(secret=Settings.secret,lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """_summary_

    Args:
        IntegerIDMixin (_type_): _description_
        BaseUserManager (_type_): _description_
    """

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """_summary_

        Args:
            password (str): _description_
            user (Union[UserCreate, User]): _description_

        Raises:
            InvalidPasswordException: _description_
            InvalidPasswordException: _description_
        """
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    # Пример метода для действий после успешной регистрации пользователя.
    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        """_summary_

        Args:
            user (User): _description_
            request (Optional[Request], optional): _description_. Defaults to None.
        """
        # Вместо print здесь можно было бы настроить отправку письма.
        print(f'Пользователь {user.email} зарегистрирован.')

# Корутина, возвращающая объект класса UserManager.
async def get_user_manager(user_db=Depends(get_user_db)):
    """_summary_

    Args:
        user_db (_type_, optional): _description_. Defaults to Depends(get_user_db).

    Yields:
        _type_: _description_
    """
    yield UserManager(user_db)
