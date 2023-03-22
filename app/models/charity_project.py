from sqlalchemy import Column, String, Text

from app.core.db import Base, DonationProjectBase


class CharityProject(Base, DonationProjectBase):
    """Модель благотворительного проекта."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return self.name
