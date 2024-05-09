from fastapi import Depends, HTTPException, status, Response, Request, APIRouter

from appV2.users.interfaces.REST.resources.save_user_resource import SaveUserResource
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.usecases.register_user_usecase import RegisterUserUseCase
from appV2.users.application.exceptions.user_error_message import ErrorMessageUserAlreadyExists
from appV2.users.infrastructure.dependencies.dependencies import get_register_user_usecase

router = APIRouter(
    prefix='/api/v2/users',
    tags=['Users'],
)

@router.post(
    '/',
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

    response.headers['location'] = f"{request.url.path}{user.id}"
    return user