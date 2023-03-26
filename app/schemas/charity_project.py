from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator, PositiveInt


class CharityProjectBase(BaseModel):
    """Базовый класс для проекта."""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None,)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    """Схема создания проекта."""
    name: str = Field(..., max_length=100)
    description: str = Field(...,)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """Схема обновления проекта."""

    @validator('name')
    def name_cannot_be_null(cls, value: str):
        if value is None:
            raise ValueError('Имя не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectBase):
    """Схема response для проекта."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime = Field(None,)

    class Config:
        orm_mode = True
