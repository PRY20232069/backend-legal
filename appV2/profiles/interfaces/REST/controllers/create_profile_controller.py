from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer

from typing import Tuple

from appV2.profiles.interfaces.REST.controllers.profiles_controller import router
from appV2.profiles.interfaces.REST.resources.save_profile_resource import SaveProfileResource
from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.model.usecases.create_profile_usecase import CreateProfileUseCase
from appV2.profiles.infrastructure.dependencies.dependencies import get_create_profile_usecase
from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError
from appV2._shared.application.exceptions.app_error_message import ErrorMessageTokenNotFound
from appV2.profiles.application.exceptions.profile_exceptions import ProfileAlreadyExistsError
from appV2.profiles.application.exceptions.profile_error_message import ErrorMessageProfileAlreadyExists

@router.post(
    '/',
    summary='Create a new profile',
    response_model=ProfileResource,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorMessageTokenNotFound
        },
        status.HTTP_409_CONFLICT: {
            'model': ErrorMessageProfileAlreadyExists
        }
    },
)
def create_profile(
    data: SaveProfileResource,
    response: Response,
    request: Request,
    token: str = Depends(HTTPBearer()),
    create_profile_usecase: CreateProfileUseCase = Depends(get_create_profile_usecase),
):
    try:
        profile = create_profile_usecase((token, data))
    except TokenNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exception.message
        )
    except ProfileAlreadyExistsError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exception.message
        )
    except Exception as _exception:
        print(_exception)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return profile