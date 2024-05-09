from typing import cast, Tuple

from appV2.users.interfaces.REST.resources.save_user_resource import SaveUserResource
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.entities.user import User
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.users.domain.repositories.user_repository import UserRepository
from appV2.users.domain.model.usecases.register_user_usecase import RegisterUserUseCase
from appV2.users.application.exceptions.user_exceptions import UserAlreadyExistsError


class RegisterUserUseCaseImpl(RegisterUserUseCase):

    def __init__(self, unit_of_work: UnitOfWork, user_repository: UserRepository):
        self.unit_of_work = unit_of_work
        self.user_repository = user_repository

    def __call__(self, args: Tuple[SaveUserResource]) -> UserResource:
        data, = args

        user = User(
            id=None,
            **data.dict()
        )

        existing_user = self.user_repository.find_by_email(data.email)
        if existing_user is not None:
            raise UserAlreadyExistsError()

        try:
            self.user_repository.create(user)
        except Exception as _e:
            self.unit_of_work.rollback()
            raise

        self.unit_of_work.commit()

        created_user = self.user_repository.find_by_email(data.email)

        return UserResource.from_entity(created_user)