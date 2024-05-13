from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy import Boolean, Column, Integer, TIMESTAMP, ForeignKey, String
from sqlalchemy.sql import func

from appV2._shared.domain.model.entities.base_entity import Base

from utils.constants import MAX_CHARS_ONE_LINE, MAX_CHARS_URL


class Contract(Base):
    __tablename__ = 'contracts'

    id: Mapped[int] | int = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)
    favorite: Mapped[bool] | bool = Column(Boolean, default=False, nullable=False)
    file_url: Mapped[str] | str | None = Column(String(MAX_CHARS_URL), nullable=True)
    uploaded_date: Mapped[datetime] | datetime = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    profile_id: int = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    bank_id: int = Column(Integer, ForeignKey('banks.id'), nullable=False)