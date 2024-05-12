from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer

from typing import List

from appV2.users.interfaces.REST.controllers.users_controller import router
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.usecases.get_all_users_usecase import GetAllUsersUseCase
from appV2.users.infrastructure.dependencies.dependencies import get_get_all_users_usecase
from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError
from appV2._shared.application.exceptions.app_error_message import ErrorMessageTokenNotFound

@router.get(
    '/all',
    summary='Get all users',
    response_model=List[UserResource],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorMessageTokenNotFound
        },
    },
)
def get_all_users(
    response: Response,
    request: Request,
    token: str = Depends(HTTPBearer()),
    get_all_users_usecase: GetAllUsersUseCase = Depends(get_get_all_users_usecase),
):
    try:
        users = get_all_users_usecase((token, ))
    except TokenNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exception.message
        )
    except Exception as _exception:
        print(_exception)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return users