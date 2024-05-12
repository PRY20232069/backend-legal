from typing import Tuple

from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.profiles.domain.model.usecases.get_profile_usecase import GetProfileUseCase
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError

from utils.jwt_utils import JwtUtils

class GetProfileUseCaseImpl(GetProfileUseCase):

    def __init__(
        self, profile_repository: ProfileRepository
    ):
        self.profile_repository = profile_repository

    def __call__(self, args: Tuple[str]) -> ProfileResource:
        token, = args
        user_id = JwtUtils.getUserId(token)

        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile is None:
            raise ProfileNotFoundError()

        return ProfileResource.from_entity(existing_profile)