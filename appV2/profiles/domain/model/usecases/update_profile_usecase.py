from abc import abstractmethod
from typing import Tuple
from fastapi.security import HTTPAuthorizationCredentials

from appV2.profiles.interfaces.REST.resources.save_profile_resource import SaveProfileResource
from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.users.domain.repositories.user_repository import UserRepository


class UpdateProfileUseCase(BaseUseCase[Tuple[HTTPAuthorizationCredentials, SaveProfileResource], ProfileResource]):

    unit_of_work: UnitOfWork
    profile_repository: ProfileRepository
    user_repository: UserRepository

    @abstractmethod
    def __call__(self, args: Tuple[HTTPAuthorizationCredentials, SaveProfileResource]) -> ProfileResource:
        raise NotImplementedError()