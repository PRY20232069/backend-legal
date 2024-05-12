from typing import Tuple, List

from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.profiles.domain.model.usecases.get_all_profiles_usecase import GetAllProfilesUseCase

from utils.jwt_utils import JwtUtils

class GetAllProfilesUseCaseImpl(GetAllProfilesUseCase):

    def __init__(
        self, profile_repository: ProfileRepository
    ):
        self.profile_repository = profile_repository

    def __call__(self, args: Tuple[str]) -> List[ProfileResource]:
        token, = args
        user_id = JwtUtils.getUserId(token)

        existing_profiles = self.profile_repository.findall()

        return [ProfileResource.from_entity(profile) for profile in existing_profiles]