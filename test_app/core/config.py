"""config_file"""
from pydantic_settings import BaseSettings
from pydantic import EmailStr
from typing import Optional


class Settings(BaseSettings):
    """_summary_

    Args:
        BaseSettings (_type_): _description_
    """
    app_title: str
    database_url: str
    secret: str = "SECRET"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config: # pylint: disable=C0115
        env_file = '.env'
