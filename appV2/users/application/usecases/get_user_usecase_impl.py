from typing import Tuple

from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2.users.domain.model.usecases.get_user_usecase import GetUserUseCase
from appV2.users.application.exceptions.user_exceptions import UsersNotFoundError

from utils.jwt_utils import JwtUtils

class GetUserUseCaseImpl(GetUserUseCase):

    def __init__(
        self, user_repository: UserRepository
    ):
        self.user_repository = user_repository

    def __call__(self, args: Tuple[str]) -> UserResource:
        token, = args
        user_id = JwtUtils.getUserId(token)

        existing_user = self.user_repository.find_by_id(user_id)
        if existing_user is None:
            raise UsersNotFoundError()

        return UserResource.from_entity(existing_user)