from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from typing import Sequence

from appV2.profiles.domain.model.entities.profile import Profile
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository


class ProfileRepositoryImpl(ProfileRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_by_user_id(self, user_id: int) -> Profile | None:
        try:
            result = self.session.query(Profile).filter(Profile.user_id == user_id).one()
        except NoResultFound:
            result = None
        return result

    def findall(self) -> Sequence[Profile]:
        statement = select(Profile)
        try:
            result: Sequence[Profile] = self.session.execute(statement).scalars().all()
        except NoResultFound:
            return []
        return result

    def update(self, profile: Profile) -> Profile:
        update_data = profile.to_dict()
        update_data.pop(Profile.created_at.key)

        statement = update(
            Profile
        ).where(
            Profile.id == profile.id
        ).values(
            update_data
        )

        self.session.execute(statement)
        return profile