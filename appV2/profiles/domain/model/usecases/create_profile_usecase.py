from abc import abstractmethod
from typing import Tuple

from appV2.profiles.interfaces.REST.resources.save_profile_resource import SaveProfileResource
from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork


class CreateProfileUseCase(BaseUseCase[Tuple[str, SaveProfileResource], ProfileResource]):

    unit_of_work: UnitOfWork
    profile_repository: ProfileRepository

    @abstractmethod
    def __call__(self, args: Tuple[str, SaveProfileResource]) -> ProfileResource:
        raise NotImplementedError()