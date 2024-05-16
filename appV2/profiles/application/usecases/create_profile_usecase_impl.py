from typing import Tuple

from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.profiles.interfaces.REST.resources.save_profile_resource import SaveProfileResource
from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.model.entities.profile import Profile
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.profiles.domain.model.usecases.create_profile_usecase import CreateProfileUseCase
from appV2.profiles.application.exceptions.profile_exceptions import ProfileAlreadyExistsError, CreateProfileError
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2.users.application.exceptions.user_exceptions import UserNotFoundError

from utils.jwt_utils import JwtUtils

class CreateProfileUseCaseImpl(CreateProfileUseCase):

    def __init__(
        self, unit_of_work: UnitOfWork, 
        profile_repository: ProfileRepository,
        user_repository: UserRepository
    ):
        self.unit_of_work = unit_of_work
        self.profile_repository = profile_repository
        self.user_repository = user_repository

    def __call__(self, args: Tuple[str, SaveProfileResource]) -> ProfileResource:
        token, data = args
        user_id = JwtUtils.get_user_id(token)

        profile = Profile(
            id=None,
            **data.dict(),
            user_id=user_id
        )

        existing_user = self.user_repository.find_by_id(user_id)
        if existing_user is None:
            raise UserNotFoundError()

        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile is not None:
            raise ProfileAlreadyExistsError()

        try:
            self.profile_repository.create(profile)
            self.unit_of_work.commit()
        except Exception as _e:
            self.unit_of_work.rollback()
            raise CreateProfileError()

        created_profile = self.profile_repository.find_by_user_id(user_id)

        profile_resource = ProfileResource.from_entity(created_profile)
        profile_resource.email = existing_user.email

        return profile_resource