from typing import Tuple, List

from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2.users.domain.model.usecases.get_all_users_usecase import GetAllUsersUseCase

from utils.jwt_utils import JwtUtils

class GetAllUsersUseCaseImpl(GetAllUsersUseCase):

    def __init__(
        self, user_repository: UserRepository
    ):
        self.user_repository = user_repository

    def __call__(self, args: Tuple[str]) -> List[UserResource]:
        token, = args
        user_id = JwtUtils.get_user_id(token)

        existing_users = self.user_repository.findall()

        return [UserResource.from_entity(user) for user in existing_users]