"""schemas for reservations"""
from datetime import datetime
from pydantic import BaseModel,field_validator,model_validator


class ReservationBase(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    from_reserve : datetime
    to_reserve : datetime

    class Config:
        """_summary_
        """
        extra = "forbid"

class ReservationUpdate(ReservationBase):
    """_summary_

    Args:
        ReservationBase (_type_): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """

    @field_validator('from_reserve')
    def check_from_reserve_later_than_now(cls,value): #pylint: disable=E0213
        """_summary_

        Args:
            value (_type_): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if value.tzinfo is not None:  # Если есть часовой пояс
            value = value.replace(tzinfo=None)  # Удаляем его
        if value <= datetime.now():
            raise ValueError("Время начала бронирования должно быть большего текущего")
        return value

    @model_validator(mode='after')
    def check_from_reserve_less_than_to_reserve(self):  # Note: changed from cls to self
        """_summary_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if self.from_reserve >= self.to_reserve:  # Access attributes directly
            raise ValueError("Время начала бронирования должно быть меньше времени окончания")
        return self

class ReservationCreate(ReservationUpdate):
    """_summary_

    Args:
        ReservationUpdate (_type_): _description_
    """
    meetingroom_id : int

class ReservationDB(ReservationBase):
    """_summary_

    Args:
        ReservationBase (_type_): _description_
    """
    id : int
    meetingroom_id : int

    class Config:
        """_summary_
        """
        from_attributes = True
