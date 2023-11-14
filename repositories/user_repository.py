from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from models.user import User
from sqlalchemy.exc import OperationalError

class UserRepository:

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def find_all(self) -> Sequence[User]:
        statement = select(User)

        try:
            result: Sequence[User] = self.session.execute(statement).scalars().all()
            return result
        except NoResultFound:
            return []
        except OperationalError:
            self.session.rollback()
            result: Sequence[User] = self.session.execute(statement).scalars().all()
            return result
        
    def find_by_id(self, id: int) -> User | None:
        statement = select(User).where(User.id == id)

        try:
            result: User = self.session.execute(statement).scalar_one()
            return result
        except NoResultFound:
            return None
        except OperationalError:
            self.session.rollback()
            result: User = self.session.execute(statement).scalar_one()
            return result
        
    def find_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        try:
            result: User = self.session.execute(statement).scalar_one()
            return result
        except NoResultFound:
            return None
        except OperationalError:
            self.session.rollback()
            result: User = self.session.execute(statement).scalar_one()
            return result