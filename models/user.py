from sqlalchemy.orm import Mapped
from sqlalchemy import String, Column, Integer
from models.base.base_entity import Base
from resources.responses.user_resource import UserResource
from utils.constants import MAX_CHARS_ONE_LINE


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] | int = Column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)
    password: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)

    def to_resource(self) -> UserResource:
        return UserResource(
            id=self.id,
            email=self.email,
            token=''
        )