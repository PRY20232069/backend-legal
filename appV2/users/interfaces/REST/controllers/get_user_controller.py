from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2.users.interfaces.REST.controllers.users_controller import router
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.usecases.get_user_usecase import GetUserUseCase
from appV2.users.infrastructure.dependencies.dependencies import get_get_user_usecase
from appV2.users.application.exceptions.user_exceptions import UserNotFoundError
from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError

@router.get(
    '',
    summary='Get user',
    response_model=UserResource,
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        UserNotFoundError().status_code: UserNotFoundError().get_response_model(),
    },
)
def get_user(
    response: Response,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    get_user_usecase: GetUserUseCase = Depends(get_get_user_usecase),
):
    user = get_user_usecase((token, ))
    return user