from abc import abstractmethod
from typing import Tuple

from appV2.users.interfaces.REST.resources.save_user_resource import SaveUserResource
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2.users.domain.services.password_hasher_service import PasswordHasherService
from appV2.users.domain.services.token_generator_service import TokenGeneratorService
from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork


class RegisterUserUseCase(BaseUseCase[Tuple[SaveUserResource], UserResource]):

    unit_of_work: UnitOfWork
    user_repository: UserRepository
    password_hasher_service: PasswordHasherService
    token_generator_service: TokenGeneratorService

    @abstractmethod
    def __call__(self, args: Tuple[SaveUserResource]) -> UserResource:
        raise NotImplementedError()