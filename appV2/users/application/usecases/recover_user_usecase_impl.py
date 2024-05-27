from typing import Tuple

from appV2.users.interfaces.REST.resources.recover_user_resource import RecoverUserResource
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.entities.user import User
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2.users.domain.model.usecases.recover_user_usecase import RecoverUserUseCase
from appV2.users.application.exceptions.user_exceptions import UserNotFoundError, RecoverUserError, EmailError
from appV2.users.domain.services.password_hasher_service import PasswordHasherService
from appV2.users.domain.services.email_service import EmailService

from settings import RECOVERY_EMAIL_SUBJECT, RECOVERY_EMAIL_CONTENT, DEFAULT_USER_PASSWORD

class RecoverUserUseCaseImpl(RecoverUserUseCase):

    def __init__(
        self, unit_of_work: UnitOfWork, 
        user_repository: UserRepository, 
        password_hasher_service: PasswordHasherService,
        email_service: EmailService,
    ):
        self.unit_of_work = unit_of_work
        self.user_repository = user_repository
        self.password_hasher_service = password_hasher_service
        self.email_service = email_service

    def __call__(self, args: Tuple[RecoverUserResource]) -> UserResource:
        data, = args

        existing_user = self.user_repository.find_by_email(data.email)
        if existing_user is None:
            raise UserNotFoundError()

        existing_user.password = self.password_hasher_service.hash(DEFAULT_USER_PASSWORD)

        try:
            self.user_repository.update(existing_user)

            self.email_service.send_email(
                to=[existing_user.email],
                subject=RECOVERY_EMAIL_SUBJECT,
                body=f'{RECOVERY_EMAIL_CONTENT} {DEFAULT_USER_PASSWORD}',
            )

            self.unit_of_work.commit()
        except EmailError as _e:
            self.unit_of_work.rollback()
            raise EmailError()
        except Exception as _e:
            self.unit_of_work.rollback()
            raise RecoverUserError()

        recovered_user = self.user_repository.find_by_email(data.email)

        user_resource = UserResource.from_entity(recovered_user)
        return user_resource