from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text
)

from app.core.db import Base, DonationProjectBase


class Donation(Base, DonationProjectBase):
    """Модель пожертвования."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text,)

    def __repr__(self):
        return f'Пожертвование №{self.id}'
