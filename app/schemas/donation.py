from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationBase(BaseModel):
    """Базовый класс для пожертвования."""
    full_amount: Optional[PositiveInt]
    comment: Optional[str] = Field(None, min_length=1)

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    """Схема создания пожертвования."""
    full_amount: PositiveInt


class DonationUserCaseDB(DonationBase):
    """Схема response пожертвования для пользователя."""
    create_date: datetime
    id: int

    class Config:
        orm_mode = True


class DonationSuperuserCaseDB(DonationUserCaseDB):
    """Схема response пожертвования для суперпользователя."""
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: datetime = Field(None,)
