from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy import String, Column, Integer

from appV2._shared.domain.model.entities.base_entity import Base

from utils.constants import MAX_CHARS_ONE_LINE


class Bank(Base):
    __tablename__ = 'banks'

    id: Mapped[int] | int = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)