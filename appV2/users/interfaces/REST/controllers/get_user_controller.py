from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer

from appV2.users.interfaces.REST.controllers.users_controller import router
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.usecases.get_user_usecase import GetUserUseCase
from appV2.users.infrastructure.dependencies.dependencies import get_get_user_usecase
from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError
from appV2._shared.application.exceptions.app_error_message import ErrorMessageTokenNotFound
from appV2.users.application.exceptions.user_exceptions import UsersNotFoundError
from appV2.users.application.exceptions.user_error_message import ErrorMessageUserNotFound

@router.get(
    '/',
    summary='Get user',
    response_model=UserResource,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorMessageTokenNotFound
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorMessageUserNotFound
        },
    },
)
def get_user(
    response: Response,
    request: Request,
    token: str = Depends(HTTPBearer()),
    get_user_usecase: GetUserUseCase = Depends(get_get_user_usecase),
):
    try:
        user = get_user_usecase((token, ))
    except TokenNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exception.message
        )
    except UsersNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exception.message
        )
    except Exception as _exception:
        print(_exception)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return user