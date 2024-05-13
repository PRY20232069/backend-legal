from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy import String, Column, Integer, TIMESTAMP, ForeignKey

from appV2._shared.domain.model.entities.base_entity import Base

from utils.constants import MAX_CHARS_ONE_LINE

class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] | int = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)
    last_name: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)
    birth_date: Mapped[datetime] | datetime = Column(TIMESTAMP, nullable=False)
    district: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)
    region: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)
    created_at: Mapped[datetime] | datetime = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    user_id: Mapped[int] | int = Column(Integer, ForeignKey('users.id'), nullable=False)