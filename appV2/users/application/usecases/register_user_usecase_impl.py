from typing import Tuple

from appV2.users.interfaces.REST.resources.save_user_resource import SaveUserResource
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.entities.user import User
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2.users.domain.model.usecases.register_user_usecase import RegisterUserUseCase
from appV2.users.application.exceptions.user_exceptions import UserAlreadyExistsError
from appV2.users.domain.services.password_hasher_service import PasswordHasherService
from appV2.users.domain.services.token_generator_service import TokenGeneratorService

class RegisterUserUseCaseImpl(RegisterUserUseCase):

    def __init__(
        self, unit_of_work: UnitOfWork, 
        user_repository: UserRepository, 
        password_hasher_service: PasswordHasherService,
        token_generator_service: TokenGeneratorService
    ):
        self.unit_of_work = unit_of_work
        self.user_repository = user_repository
        self.password_hasher_service = password_hasher_service
        self.token_generator_service = token_generator_service

    def __call__(self, args: Tuple[SaveUserResource]) -> UserResource:
        data, = args

        user = User(
            id=None,
            **data.dict()
        )

        existing_user = self.user_repository.find_by_email(data.email)
        if existing_user is not None:
            raise UserAlreadyExistsError()

        user.password = self.password_hasher_service.hash(user.password)

        try:
            self.user_repository.create(user)
        except Exception as _e:
            self.unit_of_work.rollback()
            raise

        self.unit_of_work.commit()

        created_user = self.user_repository.find_by_email(data.email)

        user_resource = UserResource.from_entity(created_user)
        user_resource.token = self.token_generator_service.generate(created_user.id)

        return user_resource