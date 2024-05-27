from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy import String, Column, Integer

from appV2._shared.domain.model.entities.base_entity import Base

from utils.constants import MAX_CHARS_ONE_LINE, MAX_CHARS_URL


class Bank(Base):
    __tablename__ = 'banks'

    id: Mapped[int] | int = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False, unique=True)
    logo_url: Mapped[str] | str = Column(String(MAX_CHARS_URL), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo_url': self.logo_url,
        }