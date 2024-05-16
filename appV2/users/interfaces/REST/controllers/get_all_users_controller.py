from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from typing import List

from appV2.users.interfaces.REST.controllers.users_controller import router
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.usecases.get_all_users_usecase import GetAllUsersUseCase
from appV2.users.infrastructure.dependencies.dependencies import get_get_all_users_usecase
from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError

@router.get(
    '/all',
    summary='Get all users',
    response_model=List[UserResource],
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
    },
)
def get_all_users(
    response: Response,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    get_all_users_usecase: GetAllUsersUseCase = Depends(get_get_all_users_usecase),
):
    users = get_all_users_usecase((token, ))
    return users