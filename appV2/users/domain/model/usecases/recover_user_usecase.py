from abc import abstractmethod
from typing import Tuple

from appV2.users.interfaces.REST.resources.recover_user_resource import RecoverUserResource
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2.users.domain.services.email_service import EmailService
from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork


class RecoverUserUseCase(BaseUseCase[Tuple[RecoverUserResource], UserResource]):

    unit_of_work: UnitOfWork
    user_repository: UserRepository
    email_service: EmailService

    @abstractmethod
    def __call__(self, args: Tuple[RecoverUserResource]) -> UserResource:
        raise NotImplementedError()