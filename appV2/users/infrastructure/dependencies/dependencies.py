from fastapi import Depends
from sqlalchemy.orm import Session

from appV2.users.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2._shared.infrastructure.configuration.database import get_session
from appV2._shared.infrastructure.dependencies.dependencies import get_unit_of_work
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.users.domain.services.password_hasher_service import PasswordHasherService
from appV2.users.infrastructure.services.password_hasher_service_impl import PasswordHasherServiceImpl
from appV2.users.domain.services.token_generator_service import TokenGeneratorService
from appV2.users.infrastructure.services.token_generator_service_impl import TokenGeneratorServiceImpl
from appV2.users.domain.services.email_service import EmailService
from appV2.users.infrastructure.services.email_service_impl import EmailServiceImpl
from appV2.users.application.usecases.register_user_usecase_impl import RegisterUserUseCaseImpl
from appV2.users.domain.model.usecases.register_user_usecase import RegisterUserUseCase
from appV2.users.application.usecases.recover_user_usecase_impl import RecoverUserUseCaseImpl
from appV2.users.domain.model.usecases.recover_user_usecase import RecoverUserUseCase
from appV2.users.application.usecases.login_user_usecase_impl import LoginUserUseCaseImpl
from appV2.users.domain.model.usecases.login_user_usecase import LoginUserUseCase
from appV2.users.application.usecases.get_user_usecase_impl import GetUserUseCaseImpl
from appV2.users.domain.model.usecases.get_user_usecase import GetUserUseCase
from appV2.users.application.usecases.get_all_users_usecase_impl import GetAllUsersUseCaseImpl
from appV2.users.domain.model.usecases.get_all_users_usecase import GetAllUsersUseCase


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepositoryImpl(session)

def get_password_hasher_service() -> PasswordHasherService:
    return PasswordHasherServiceImpl()

def get_token_generator_service() -> TokenGeneratorService:
    return TokenGeneratorServiceImpl()

def get_email_service() -> EmailService:
    return EmailServiceImpl()

def get_register_user_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    user_repository: UserRepository = Depends(get_user_repository),
    password_hasher_service: PasswordHasherService = Depends(get_password_hasher_service),
    token_generator_service: TokenGeneratorService = Depends(get_token_generator_service)
) -> RegisterUserUseCase:
    return RegisterUserUseCaseImpl(
        unit_of_work, 
        user_repository, 
        password_hasher_service, 
        token_generator_service
    )

def get_recover_user_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    user_repository: UserRepository = Depends(get_user_repository),
    password_hasher_service: PasswordHasherService = Depends(get_password_hasher_service),
    email_service: EmailService = Depends(get_email_service),
) -> RecoverUserUseCase:
    return RecoverUserUseCaseImpl(
        unit_of_work, 
        user_repository, 
        password_hasher_service,
        email_service,
    )

def get_login_user_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
    password_hasher_service: PasswordHasherService = Depends(get_password_hasher_service),
    token_generator_service: TokenGeneratorService = Depends(get_token_generator_service)
) -> LoginUserUseCase:
    return LoginUserUseCaseImpl(
        user_repository, 
        password_hasher_service, 
        token_generator_service
    )

def get_get_user_usecase(
    user_repository: UserRepository = Depends(get_user_repository)
) -> GetUserUseCase:
    return GetUserUseCaseImpl(
        user_repository
    )

def get_get_all_users_usecase(
    user_repository: UserRepository = Depends(get_user_repository)
) -> GetAllUsersUseCase:
    return GetAllUsersUseCaseImpl(
        user_repository
    )