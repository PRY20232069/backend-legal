from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError
from appV2._shared.application.exceptions.app_error_message import ErrorMessageTokenNotFound
from appV2.profiles.interfaces.REST.controllers.profiles_controller import router
from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.model.usecases.get_profile_usecase import GetProfileUseCase
from appV2.profiles.infrastructure.dependencies.dependencies import get_get_profile_usecase
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.profiles.application.exceptions.profile_error_message import ErrorMessageProfileNotFound

@router.get(
    '/',
    summary='Get profile',
    response_model=ProfileResource,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorMessageTokenNotFound
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorMessageProfileNotFound
        },
    },
)
def get_profile(
    response: Response,
    request: Request,
    token: str = Depends(HTTPBearer()),
    get_profile_usecase: GetProfileUseCase = Depends(get_get_profile_usecase),
):
    try:
        profile = get_profile_usecase((token, ))
    except TokenNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exception.message
        )
    except ProfileNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exception.message
        )
    except Exception as _exception:
        print(_exception)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return profile