from fastapi import Depends
from sqlalchemy.orm import Session

from appV2.users.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2.users.application.usecases.register_user_usecase_impl import RegisterUserUseCaseImpl
from appV2.users.domain.model.usecases.register_user_usecase import RegisterUserUseCase
from appV2._shared.infrastructure.configuration.database import get_session
from appV2._shared.infrastructure.dependencies.dependencies import get_unit_of_work
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepositoryImpl(session)

def get_register_user_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work)
) -> RegisterUserUseCase:
    return RegisterUserUseCaseImpl(unit_of_work)