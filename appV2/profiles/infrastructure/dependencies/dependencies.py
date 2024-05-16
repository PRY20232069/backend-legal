from fastapi import Depends
from sqlalchemy.orm import Session

from appV2._shared.infrastructure.configuration.database import get_session
from appV2._shared.infrastructure.dependencies.dependencies import get_unit_of_work
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.profiles.infrastructure.repositories.profile_repository_impl import ProfileRepositoryImpl
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.profiles.application.usecases.create_profile_usecase_impl import CreateProfileUseCaseImpl
from appV2.profiles.domain.model.usecases.create_profile_usecase import CreateProfileUseCase
from appV2.profiles.application.usecases.get_profile_usecase_impl import GetProfileUseCaseImpl
from appV2.profiles.domain.model.usecases.get_profile_usecase import GetProfileUseCase
from appV2.profiles.application.usecases.get_all_profiles_usecase_impl import GetAllProfilesUseCaseImpl
from appV2.profiles.domain.model.usecases.get_all_profiles_usecase import GetAllProfilesUseCase
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2.users.infrastructure.dependencies.dependencies import get_user_repository


def get_profile_repository(session: Session = Depends(get_session)) -> ProfileRepository:
    return ProfileRepositoryImpl(session)

def get_create_profile_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    profile_repository: ProfileRepository = Depends(get_profile_repository),
    user_repository: UserRepository = Depends(get_user_repository)
) -> CreateProfileUseCaseImpl:
    return CreateProfileUseCaseImpl(
        unit_of_work, 
        profile_repository,
        user_repository
    )

def get_get_profile_usecase(
    profile_repository: ProfileRepository = Depends(get_profile_repository),
    user_repository: UserRepository = Depends(get_user_repository)
) -> GetProfileUseCase:
    return GetProfileUseCaseImpl(
        profile_repository,
        user_repository
    )

def get_get_all_profiles_usecase(
    profile_repository: ProfileRepository = Depends(get_profile_repository),
    user_repository: UserRepository = Depends(get_user_repository)
) -> GetAllProfilesUseCase:
    return GetAllProfilesUseCaseImpl(
        profile_repository,
        user_repository
    )