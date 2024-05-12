from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer

from typing import List

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError
from appV2._shared.application.exceptions.app_error_message import ErrorMessageTokenNotFound
from appV2.profiles.interfaces.REST.controllers.profiles_controller import router
from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.model.usecases.get_all_profiles_usecase import GetAllProfilesUseCase
from appV2.profiles.infrastructure.dependencies.dependencies import get_get_all_profiles_usecase

@router.get(
    '/all',
    summary='Get all profiles',
    response_model=List[ProfileResource],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorMessageTokenNotFound
        },
    },
)
def get_all_profiles(
    response: Response,
    request: Request,
    token: str = Depends(HTTPBearer()),
    get_all_profiles_usecase: GetAllProfilesUseCase = Depends(get_get_all_profiles_usecase),
):
    try:
        profiles = get_all_profiles_usecase((token, ))
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

    return profiles