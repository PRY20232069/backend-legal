from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy import String, Column, Integer, TIMESTAMP, ForeignKey

from appV2._shared.domain.model.entities.base_entity import Base

from utils.constants import MAX_CHARS_ONE_LINE, MAX_CHARS_ONE_LINE_SUPER_SMALL

class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] | int = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)
    last_name: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)
    birth_date: Mapped[datetime] | datetime = Column(TIMESTAMP, nullable=False)
    district: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)
    region: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)
    gender: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE_SUPER_SMALL), nullable=False)
    document_number: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE_SUPER_SMALL), nullable=False)
    created_at: Mapped[datetime] | datetime = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    user_id: Mapped[int] | int = Column(Integer, ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'district': self.district,
            'region': self.region,
            'gender': self.gender,
            'document_number': self.document_number,
            'created_at': self.created_at,
            'user_id': self.user_id
        }