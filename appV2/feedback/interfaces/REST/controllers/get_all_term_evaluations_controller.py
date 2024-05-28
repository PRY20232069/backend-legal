from typing import Tuple, List
from fastapi import Depends, HTTPException, status, Response, Request, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.feedback.interfaces.REST.controllers.feedback_controller import router
from appV2.feedback.interfaces.REST.resources.term_evaluation_resource import TermEvaluationResource
from appV2.feedback.domain.model.usecases.get_all_term_evaluations_usecase import GetAllTermEvaluationsUseCase
from appV2.feedback.infrastructure.dependencies.dependencies import get_get_all_term_evaluations_usecase

@router.get(
    '/terms/all}',
    summary='Get all term evaluations',
    response_model=List[TermEvaluationResource],
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        ProfileNotFoundError().status_code: ProfileNotFoundError().get_response_model(),
    },
)
async def get_all_term_evaluations(
    response: Response,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    get_all_term_evaluations_usecase: GetAllTermEvaluationsUseCase = Depends(get_get_all_term_evaluations_usecase),
):
    term_evaluation = await get_all_term_evaluations_usecase((token, ))
    return term_evaluation