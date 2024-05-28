from typing import Tuple
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2._shared.application.exceptions.app_exceptions import TokenInvalidError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.contracts.application.exceptions.term_exceptions import TermNotFoundError
from appV2.contracts.domain.repositories.term_repository import TermRepository
from appV2.feedback.interfaces.REST.resources.save_term_evaluation_resource import SaveTermEvaluationResource
from appV2.feedback.interfaces.REST.resources.term_evaluation_resource import TermEvaluationResource
from appV2.feedback.domain.model.entities.term_evaluation import TermEvaluation
from appV2.feedback.domain.repositories.term_evaluation_repository import TermEvaluationRepository
from appV2.feedback.domain.model.usecases.create_term_evaluation_usecase import CreateTermEvaluationUseCase
from appV2.feedback.application.exceptions.term_evaluation_exceptions import TermEvaluationAlreadyExistsError, CreateTermEvaluationError

from utils.jwt_utils import JwtUtils

class CreateTermEvaluationUseCaseImpl(CreateTermEvaluationUseCase):

    def __init__(
        self, unit_of_work: UnitOfWork, 
        term_evaluation_repository: TermEvaluationRepository,
        term_repository: TermRepository,
        profile_repository: ProfileRepository,
    ):
        self.unit_of_work = unit_of_work
        self.term_evaluation_repository = term_evaluation_repository
        self.term_repository = term_repository
        self.profile_repository = profile_repository

    async def __call__(self, args: Tuple[Tuple[HTTPAuthorizationCredentials, int], SaveTermEvaluationResource]) -> TermEvaluationResource:
        identifiers, data = args
        token, term_id = identifiers

        if not JwtUtils.is_valid(token):
            raise TokenInvalidError()

        user_id = JwtUtils.get_user_id(token)

        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile is None:
            raise ProfileNotFoundError()

        existing_term = self.term_repository.find_by_id(term_id)
        if existing_term is None:
            raise TermNotFoundError()

        existing_term_evaluation = self.term_evaluation_repository.find_by_term_id_and_profile_id(term_id, existing_profile.id)
        if existing_term_evaluation is not None:
            raise TermEvaluationAlreadyExistsError()

        term_evaluation = TermEvaluation(
            id=None,
            **data.dict(),
            profile_id=existing_profile.id,
            term_id=term_id,
        )

        try:
            self.term_evaluation_repository.create(term_evaluation)
            self.unit_of_work.commit()
        except Exception as _e:
            self.unit_of_work.rollback()
            raise CreateTermEvaluationError()

        created_term_evaluation = self.term_evaluation_repository.find_by_term_id_and_profile_id(term_id, existing_profile.id)

        return TermEvaluationResource.from_entity(created_term_evaluation)