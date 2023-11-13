from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from models.profile import Profile

class ProfileRepository:

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, profile: Profile) -> Profile:
        self.session.add(profile)
        self.session.commit()
        self.session.refresh(profile)
        return profile

    def find_all(self) -> Sequence[Profile]:
        statement = select(Profile)

        try:
            result: Sequence[Profile] = self.session.execute(statement).scalars().all()
            return result
        except NoResultFound:
            return []
    
    def find_by_user_id(self, user_id: int) -> Profile | None:
        statement = select(Profile).filter(Profile.user_id == user_id)

        try:
            result: Profile = self.session.execute(statement).scalar_one()
            return result
        except NoResultFound:
            return None