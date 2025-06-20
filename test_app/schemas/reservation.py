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
        if value <= datetime.now():
            raise ValueError("Время начала бронирования должно быть большего текущего")
        return value

    @model_validator(skip_on_failure=True)
    def check_from_reserve_less_than_to_reserve(cls,values): #pylint: disable=E0213
        if values['from_reserve'] >= values['to_reserve']:
            raise ValueError("Время начала бронирования должно быть меньше времени окончания")
        return values

class ReservationCreate(ReservationUpdate):
    meetingroom_id : int

class ReservationDB(ReservationBase):
    id : int
    meetingroom_id : int

    class Config:
        from_attributes = True
