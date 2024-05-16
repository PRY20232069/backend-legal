from abc import abstractmethod
from typing import Tuple

from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2.users.domain.repositories.user_repository import UserRepository


class GetProfileUseCase(BaseUseCase[Tuple[str], ProfileResource]):

    profile_repository: ProfileRepository
    user_repository: UserRepository

    @abstractmethod
    def __call__(self, args: Tuple[str]) -> ProfileResource:
        raise NotImplementedError()