from sqlalchemy.orm import Mapped
from sqlalchemy import String, Column, Integer

from appV2._shared.domain.model.entities.base_entity import Base

from utils.constants import MAX_CHARS_ONE_LINE


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] | int = Column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False, unique=True, index=True)
    password: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password
        }