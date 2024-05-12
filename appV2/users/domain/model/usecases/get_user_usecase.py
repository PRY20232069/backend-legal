from abc import abstractmethod
from typing import Tuple

from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase


class GetUserUseCase(BaseUseCase[str, UserResource]):

    user_repository: UserRepository

    @abstractmethod
    def __call__(self, args: Tuple[str]) -> UserResource:
        raise NotImplementedError()