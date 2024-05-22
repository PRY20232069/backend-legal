from typing import Tuple
from fastapi.security import HTTPAuthorizationCredentials

from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.profiles.domain.model.usecases.get_profile_usecase import GetProfileUseCase
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.users.domain.repositories.user_repository import UserRepository

from utils.jwt_utils import JwtUtils

class GetProfileUseCaseImpl(GetProfileUseCase):

    def __init__(
        self, profile_repository: ProfileRepository,
        user_repository: UserRepository
    ):
        self.profile_repository = profile_repository
        self.user_repository = user_repository

    def __call__(self, args: Tuple[HTTPAuthorizationCredentials]) -> ProfileResource:
        token, = args
        user_id = JwtUtils.get_user_id(token)

        existing_user = self.user_repository.find_by_id(user_id)
        if existing_user is None:
            raise UserNotFoundError()

        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile is None:
            raise ProfileNotFoundError()

        profile_resource = ProfileResource.from_entity(existing_profile)
        profile_resource.email = existing_user.email
        
        return profile_resource