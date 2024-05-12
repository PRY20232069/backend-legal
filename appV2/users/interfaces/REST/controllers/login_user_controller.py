from fastapi import Depends, HTTPException, status, Response, Request, APIRouter

from appV2.users.interfaces.REST.controllers.users_controller import router
from appV2.users.interfaces.REST.resources.save_user_resource import SaveUserResource
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.usecases.login_user_usecase import LoginUserUseCase
from appV2.users.infrastructure.dependencies.dependencies import get_login_user_usecase
from appV2._shared.application.exceptions.app_exceptions import InvalidCredentialsError
from appV2._shared.application.exceptions.app_error_message import ErrorMessageInvalidCredentials
from appV2.users.application.exceptions.user_exceptions import UserNotFoundError
from appV2.users.application.exceptions.user_error_message import ErrorMessageUserNotFound

@router.post(
    '/login',
    summary='Login user',
    response_model=UserResource,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorMessageInvalidCredentials
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorMessageUserNotFound
        },
    },
)
def login_user(
    data: SaveUserResource,
    response: Response,
    request: Request,
    login_user_usecase: LoginUserUseCase = Depends(get_login_user_usecase),
):
    try:
        user = login_user_usecase((data, ))
    except InvalidCredentialsError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exception.message
        )
    except UserNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exception.message
        )
    except Exception as _exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return user