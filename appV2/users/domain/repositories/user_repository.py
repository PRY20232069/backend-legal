from abc import abstractmethod

from appV2._shared.domain.repositories.base_repository import BaseRepository
from appV2.users.domain.model.entities.user import User


class UserRepository(BaseRepository[User]):

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        raise NotImplementedError()