from abc import abstractmethod
from typing import Tuple

from fastapi.security import HTTPAuthorizationCredentials

from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork


class CreateTermUseCase(BaseUseCase[Tuple[Tuple[HTTPAuthorizationCredentials, int], UploadFile], TermResource]):

    unit_of_work: UnitOfWork
    term_repository: TermRepository
    profile_repository: ProfileRepository

    @abstractmethod
    def __call__(self, args: Tuple[Tuple[HTTPAuthorizationCredentials, int], UploadFile]) -> TermResource:
        raise NotImplementedError()