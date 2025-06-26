"""schemas for reservations"""
from datetime import datetime
from pydantic import BaseModel,field_validator,model_validator


class ReservationBase(BaseModel):
    from_reserve : datetime
    to_reserve : datetime

    class Config:
        extra = "forbid"

class ReservationUpdate(ReservationBase):

    @field_validator('from_reserve')
    def check_from_reserve_later_than_now(cls,value): #pylint: disable=E0213
        if value.tzinfo is not None:  # Если есть часовой пояс
            value = value.replace(tzinfo=None)  # Удаляем его
        if value <= datetime.now():
            raise ValueError("Время начала бронирования должно быть большего текущего")
        return value

    @model_validator(mode='after')
    def check_from_reserve_less_than_to_reserve(self):  # Note: changed from cls to self
        if self.from_reserve >= self.to_reserve:  # Access attributes directly
            raise ValueError("Время начала бронирования должно быть меньше времени окончания")
        return self

class ReservationCreate(ReservationUpdate):
    meetingroom_id : int

class ReservationDB(ReservationBase):
    id : int
    meetingroom_id : int

    class Config:
        from_attributes = True
