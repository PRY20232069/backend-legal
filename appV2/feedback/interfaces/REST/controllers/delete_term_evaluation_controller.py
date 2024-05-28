from typing import Tuple
from fastapi import Depends, HTTPException, status, Response, Request, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.contracts.application.exceptions.term_exceptions import TermNotFoundError
from appV2.feedback.application.exceptions.term_evaluation_exceptions import TermEvaluationNotFoundError, DeleteTermEvaluationError
from appV2.feedback.interfaces.REST.controllers.feedback_controller import router
from appV2.feedback.interfaces.REST.resources.term_evaluation_resource import TermEvaluationResource
from appV2.feedback.domain.model.usecases.delete_term_evaluation_usecase import DeleteTermEvaluationUseCase
from appV2.feedback.infrastructure.dependencies.dependencies import get_delete_term_evaluation_usecase

@router.delete(
    '/terms/{term_id}',
    summary='Delete a term evaluation',
    response_model=TermEvaluationResource,
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        ProfileNotFoundError().status_code: ProfileNotFoundError().get_response_model_array([
            TermNotFoundError().message,
            TermEvaluationNotFoundError().message]),
        DeleteTermEvaluationError().status_code: DeleteTermEvaluationError().get_response_model(),
    },
)
async def delete_term_evaluation(
    response: Response,
    request: Request,
    term_id: int,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    delete_term_evaluation_usecase: DeleteTermEvaluationUseCase = Depends(get_delete_term_evaluation_usecase),
):
    term_evaluation = await delete_term_evaluation_usecase((token, term_id))
    return term_evaluation