from typing import Tuple
from fastapi import Depends, HTTPException, status, Response, Request, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.contracts.application.exceptions.term_exceptions import TermNotFoundError
from appV2.feedback.application.exceptions.term_evaluation_exceptions import TermEvaluationNotFoundError, UpdateTermEvaluationError
from appV2.feedback.interfaces.REST.controllers.feedback_controller import router
from appV2.feedback.interfaces.REST.resources.save_term_evaluation_resource import SaveTermEvaluationResource
from appV2.feedback.interfaces.REST.resources.term_evaluation_resource import TermEvaluationResource
from appV2.feedback.domain.model.usecases.update_term_evaluation_usecase import UpdateTermEvaluationUseCase
from appV2.feedback.infrastructure.dependencies.dependencies import get_update_term_evaluation_usecase

@router.put(
    '/terms/{term_id}',
    summary='Update a term evaluation',
    response_model=TermEvaluationResource,
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        ProfileNotFoundError().status_code: ProfileNotFoundError().get_response_model_array([
            TermNotFoundError().message,
            TermEvaluationNotFoundError().message]),
        UpdateTermEvaluationError().status_code: UpdateTermEvaluationError().get_response_model(),
    },
)
async def update_term_evaluation(
    data: SaveTermEvaluationResource,
    response: Response,
    request: Request,
    term_id: int,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    update_term_evaluation_usecase: UpdateTermEvaluationUseCase = Depends(get_update_term_evaluation_usecase),
):
    term_evaluation = await update_term_evaluation_usecase(((token, term_id), data))
    return term_evaluation