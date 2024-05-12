from abc import abstractmethod

from appV2._shared.domain.repositories.base_repository import BaseRepository
from appV2.profiles.domain.model.entities.profile import Profile


class ProfileRepository(BaseRepository[Profile]):

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Profile | None:
        raise NotImplementedError()