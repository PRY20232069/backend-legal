from fastapi import Depends, HTTPException, status, Response, Request, APIRouter

from appV2.users.interfaces.REST.controllers.users_controller import router
from appV2.users.interfaces.REST.resources.save_user_resource import SaveUserResource
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.usecases.login_user_usecase import LoginUserUseCase
from appV2.users.infrastructure.dependencies.dependencies import get_login_user_usecase
from appV2.users.application.exceptions.user_exceptions import UserInvalidCredentialsError
from appV2.users.application.exceptions.user_exceptions import UserNotFoundError

@router.post(
    '/login',
    summary='Login user',
    response_model=UserResource,
    status_code=status.HTTP_200_OK,
    responses={
        UserInvalidCredentialsError().status_code: UserInvalidCredentialsError().get_response_model(),
        UserNotFoundError().status_code: UserNotFoundError().get_response_model(),
    },
)
def login_user(
    data: SaveUserResource,
    response: Response,
    request: Request,
    login_user_usecase: LoginUserUseCase = Depends(get_login_user_usecase),
):
    user = login_user_usecase((data, ))
    return user