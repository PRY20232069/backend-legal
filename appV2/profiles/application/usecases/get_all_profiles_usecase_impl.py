from typing import Tuple, List

from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.profiles.domain.model.usecases.get_all_profiles_usecase import GetAllProfilesUseCase
from appV2.users.domain.repositories.user_repository import UserRepository

from utils.jwt_utils import JwtUtils

class GetAllProfilesUseCaseImpl(GetAllProfilesUseCase):

    def __init__(
        self, profile_repository: ProfileRepository,
        user_repository: UserRepository
    ):
        self.profile_repository = profile_repository
        self.user_repository = user_repository

    def __call__(self, args: Tuple[str]) -> List[ProfileResource]:
        token, = args
        user_id = JwtUtils.get_user_id(token)

        existing_profiles = self.profile_repository.findall()
        profile_resources = []

        for profile in existing_profiles:
            existing_user = self.user_repository.find_by_id(profile.user_id)
            if existing_user is None:
                raise UserNotFoundError()

            profile_resource = ProfileResource.from_entity(profile)
            profile_resource.email = existing_user.email

            profile_resources.append(profile_resource)

        # return [ProfileResource.from_entity(profile) for profile in existing_profiles]
        return profile_resources