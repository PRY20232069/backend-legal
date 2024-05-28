from typing import Tuple
from fastapi import Depends, HTTPException, status, Response, Request, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.contracts.application.exceptions.term_exceptions import TermNotFoundError
from appV2.feedback.application.exceptions.term_evaluation_exceptions import TermEvaluationAlreadyExistsError, CreateTermEvaluationError
from appV2.feedback.interfaces.REST.controllers.feedback_controller import router
from appV2.feedback.interfaces.REST.resources.save_term_evaluation_resource import SaveTermEvaluationResource
from appV2.feedback.interfaces.REST.resources.term_evaluation_resource import TermEvaluationResource
from appV2.feedback.domain.model.usecases.create_term_evaluation_usecase import CreateTermEvaluationUseCase
from appV2.feedback.infrastructure.dependencies.dependencies import get_create_term_evaluation_usecase

@router.post(
    '/terms/{term_id}',
    summary='Create a new term evaluation',
    response_model=TermEvaluationResource,
    status_code=status.HTTP_201_CREATED,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        ProfileNotFoundError().status_code: ProfileNotFoundError().get_response_model_array([
            TermNotFoundError().message]),
        TermEvaluationAlreadyExistsError().status_code: TermEvaluationAlreadyExistsError().get_response_model(),
        CreateTermEvaluationError().status_code: CreateTermEvaluationError().get_response_model(),
    },
)
async def create_term_evaluation(
    data: SaveTermEvaluationResource,
    response: Response,
    request: Request,
    term_id: int,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    create_term_evaluation_usecase: CreateTermEvaluationUseCase = Depends(get_create_term_evaluation_usecase),
):
    term_evaluation = await create_term_evaluation_usecase(((token, term_id), data))
    return term_evaluation