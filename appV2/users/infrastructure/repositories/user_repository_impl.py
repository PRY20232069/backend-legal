from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from typing import Sequence

from appV2.users.domain.model.entities.user import User
from appV2.users.domain.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_by_email(self, email: str) -> User | None:
        statement = select(User).filter_by(email=email)
        try:
            result: User = self.session.execute(statement).scalar_one()
        except NoResultFound:
            return None
        return result

    def findall(self) -> Sequence[User]:
        statement = select(User)
        try:
            result: Sequence[User] = self.session.execute(statement).scalars().all()
        except NoResultFound:
            return []
        return result

    def find_by_id(self, id: int) -> User | None:
        result: User | None = self.session.get(User, id)
        return result