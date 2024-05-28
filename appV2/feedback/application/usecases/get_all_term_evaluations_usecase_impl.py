from typing import Tuple, List
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenInvalidError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.feedback.interfaces.REST.resources.term_evaluation_resource import TermEvaluationResource
from appV2.feedback.domain.model.entities.term_evaluation import TermEvaluation
from appV2.feedback.domain.repositories.term_evaluation_repository import TermEvaluationRepository
from appV2.feedback.domain.model.usecases.get_all_term_evaluations_usecase import GetAllTermEvaluationsUseCase

from utils.jwt_utils import JwtUtils

class GetAllTermEvaluationsUseCaseImpl(GetAllTermEvaluationsUseCase):

    def __init__(
        self, term_evaluation_repository: TermEvaluationRepository,
        profile_repository: ProfileRepository,
    ):
        self.term_evaluation_repository = term_evaluation_repository
        self.profile_repository = profile_repository

    async def __call__(self, args: Tuple[HTTPAuthorizationCredentials]) -> List[TermEvaluationResource]:
        token, = args

        if not JwtUtils.is_valid(token):
            raise TokenInvalidError()

        user_id = JwtUtils.get_user_id(token)

        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile is None:
            raise ProfileNotFoundError()

        term_evaluations = self.term_evaluation_repository.findall()

        return [TermEvaluationResource.from_entity(term_evaluation) for term_evaluation in term_evaluations]