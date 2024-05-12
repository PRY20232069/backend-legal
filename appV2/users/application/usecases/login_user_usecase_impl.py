from typing import Tuple

from appV2.users.interfaces.REST.resources.save_user_resource import SaveUserResource
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.entities.user import User
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2.users.domain.model.usecases.login_user_usecase import LoginUserUseCase
from appV2.users.application.exceptions.user_exceptions import UsersNotFoundError
from appV2.users.domain.services.password_hasher_service import PasswordHasherService
from appV2.users.domain.services.token_generator_service import TokenGeneratorService

class LoginUserUseCaseImpl(LoginUserUseCase):

    def __init__(
        self, user_repository: UserRepository, 
        password_hasher_service: PasswordHasherService,
        token_generator_service: TokenGeneratorService
    ):
        self.user_repository = user_repository
        self.password_hasher_service = password_hasher_service
        self.token_generator_service = token_generator_service

    def __call__(self, args: Tuple[SaveUserResource]) -> UserResource:
        data, = args

        existing_user = self.user_repository.find_by_email(data.email)
        if existing_user is None:
            raise UsersNotFoundError()

        if not self.password_hasher_service.verify(data.password, existing_user.password):
            raise HTTPException(
                status_code=400,
                detail="Invalid credentials"
            )

        user_resource = UserResource.from_entity(existing_user)
        user_resource.token = self.token_generator_service.generate(existing_user.id)

        return user_resource