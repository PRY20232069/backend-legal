from abc import abstractmethod
from typing import Tuple, List
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2.feedback.interfaces.REST.resources.term_evaluation_resource import TermEvaluationResource
from appV2.feedback.domain.repositories.term_evaluation_repository import TermEvaluationRepository
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository


class GetAllTermEvaluationsUseCase(BaseUseCase[Tuple[HTTPAuthorizationCredentials], List[TermEvaluationResource]]):

    term_evaluation_repository: TermEvaluationRepository
    profile_repository: ProfileRepository

    @abstractmethod
    def __call__(self, args: Tuple[HTTPAuthorizationCredentials]) -> List[TermEvaluationResource]:
        raise NotImplementedError()