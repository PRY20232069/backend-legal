from typing import List
from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
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
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
    },
)
def get_all_profiles(
    response: Response,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    get_all_profiles_usecase: GetAllProfilesUseCase = Depends(get_get_all_profiles_usecase),
):
    profiles = get_all_profiles_usecase((token, ))
    return profiles