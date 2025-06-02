"""config_file"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """_summary_

    Args:
        BaseSettings (_type_): _description_
    """
    app_title: str
    database_url: str

    class Config: # pylint: disable=C0115
        env_file = '.env'
