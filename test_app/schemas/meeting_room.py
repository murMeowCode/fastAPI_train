from typing import Optional

from pydantic import BaseModel, Field, field_validator


# Базовый класс схемы, от которого наследуем все остальные.
class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


# Теперь наследуем схему не от BaseModel, а от MeetingRoomBase.
class MeetingRoomCreate(MeetingRoomBase):
    # Переопределяем атрибут name, делаем его обязательным.
    name: str = Field(..., min_length=1, max_length=100)
    # Описывать поле description не нужно: оно уже есть в базовом классе.


# Возвращаемую схему унаследуем от MeetingRoomCreate, 
# чтобы снова не описывать обязательное поле name.
class MeetingRoomDB(MeetingRoomCreate):
    id: int

    class Config:
        from_attributes = True

class MeetingRoomUpdate(MeetingRoomBase):
    
    @field_validator('name')
    def name_cannot_be_null(cls, value): #pylint: disable=E0213
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value
