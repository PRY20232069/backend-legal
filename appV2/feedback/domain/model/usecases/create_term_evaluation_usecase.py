from abc import abstractmethod
from typing import Tuple
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.contracts.domain.repositories.term_repository import TermRepository
from appV2.feedback.interfaces.REST.resources.term_evaluation_resource import TermEvaluationResource
from appV2.feedback.interfaces.REST.resources.save_term_evaluation_resource import SaveTermEvaluationResource
from appV2.feedback.domain.repositories.term_evaluation_repository import TermEvaluationRepository


class CreateTermEvaluationUseCase(BaseUseCase[Tuple[Tuple[HTTPAuthorizationCredentials, int], SaveTermEvaluationResource], TermEvaluationResource]):

    unit_of_work: UnitOfWork
    term_evaluation_repository: TermEvaluationRepository
    term_repository: TermRepository
    profile_repository: ProfileRepository

    @abstractmethod
    def __call__(self, args: Tuple[Tuple[HTTPAuthorizationCredentials, int], SaveTermEvaluationResource]) -> TermEvaluationResource:
        raise NotImplementedError()