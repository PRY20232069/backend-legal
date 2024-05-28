from fastapi import Depends
from sqlalchemy.orm import Session

from appV2._shared.infrastructure.configuration.database import get_session
from appV2._shared.infrastructure.dependencies.dependencies import get_unit_of_work
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.contracts.domain.repositories.term_repository import TermRepository
from appV2.contracts.infrastructure.dependencies.dependencies import get_term_repository
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.profiles.infrastructure.dependencies.dependencies import get_profile_repository
from appV2.feedback.infrastructure.repositories.term_evaluation_repository_impl import TermEvaluationRepositoryImpl
from appV2.feedback.domain.repositories.term_evaluation_repository import TermEvaluationRepository
from appV2.feedback.application.usecases.create_term_evaluation_usecase_impl import CreateTermEvaluationUseCaseImpl
from appV2.feedback.domain.model.usecases.create_term_evaluation_usecase import CreateTermEvaluationUseCase
from appV2.feedback.application.usecases.update_term_evaluation_usecase_impl import UpdateTermEvaluationUseCaseImpl
from appV2.feedback.domain.model.usecases.update_term_evaluation_usecase import UpdateTermEvaluationUseCase
from appV2.feedback.application.usecases.delete_term_evaluation_usecase_impl import DeleteTermEvaluationUseCaseImpl
from appV2.feedback.domain.model.usecases.delete_term_evaluation_usecase import DeleteTermEvaluationUseCase
from appV2.feedback.application.usecases.get_all_term_evaluations_usecase_impl import GetAllTermEvaluationsUseCaseImpl
from appV2.feedback.domain.model.usecases.get_all_term_evaluations_usecase import GetAllTermEvaluationsUseCase


def get_term_evaluation_repository(session: Session = Depends(get_session)) -> TermEvaluationRepository:
    return TermEvaluationRepositoryImpl(session)

def get_create_term_evaluation_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    term_evaluation_repository: TermEvaluationRepository = Depends(get_term_evaluation_repository),
    term_repository: TermRepository = Depends(get_term_repository),
    profile_repository: ProfileRepository = Depends(get_profile_repository),
) -> CreateTermEvaluationUseCase:
    return CreateTermEvaluationUseCaseImpl(
        unit_of_work,
        term_evaluation_repository,
        term_repository,
        profile_repository,
    )

def get_update_term_evaluation_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    term_evaluation_repository: TermEvaluationRepository = Depends(get_term_evaluation_repository),
    term_repository: TermRepository = Depends(get_term_repository),
    profile_repository: ProfileRepository = Depends(get_profile_repository),
) -> UpdateTermEvaluationUseCase:
    return UpdateTermEvaluationUseCaseImpl(
        unit_of_work,
        term_evaluation_repository,
        term_repository,
        profile_repository,
    )

def get_delete_term_evaluation_usecase(
    term_evaluation_repository: TermEvaluationRepository = Depends(get_term_evaluation_repository),
    term_repository: TermRepository = Depends(get_term_repository),
    profile_repository: ProfileRepository = Depends(get_profile_repository),
) -> DeleteTermEvaluationUseCase:
    return DeleteTermEvaluationUseCaseImpl(
        term_evaluation_repository,
        term_repository,
        profile_repository,
    )

def get_get_all_term_evaluations_usecase(
    term_evaluation_repository: TermEvaluationRepository = Depends(get_term_evaluation_repository),
    profile_repository: ProfileRepository = Depends(get_profile_repository),
) -> GetAllTermEvaluationsUseCase:
    return GetAllTermEvaluationsUseCaseImpl(
        term_evaluation_repository,
        profile_repository,
    )