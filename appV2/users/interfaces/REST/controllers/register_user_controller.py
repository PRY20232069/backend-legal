from fastapi import Depends, HTTPException, status, Response, Request, APIRouter

from appV2.users.interfaces.REST.controllers.users_controller import router
from appV2.users.interfaces.REST.resources.save_user_resource import SaveUserResource
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.usecases.register_user_usecase import RegisterUserUseCase
from appV2.users.infrastructure.dependencies.dependencies import get_register_user_usecase
from appV2.users.application.exceptions.user_exceptions import UserAlreadyExistsError
from appV2.users.application.exceptions.user_error_message import ErrorMessageUserAlreadyExists

@router.post(
    '/register',
    summary='Register a new user',
    response_model=UserResource,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            'model': ErrorMessageUserAlreadyExists
        }
    },
)
def register_user(
    data: SaveUserResource,
    response: Response,
    request: Request,
    register_user_usecase: RegisterUserUseCase = Depends(get_register_user_usecase),
):
    try:
        user = register_user_usecase((data, ))
    except UserAlreadyExistsError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exception.message
        )
    except Exception as _exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return user