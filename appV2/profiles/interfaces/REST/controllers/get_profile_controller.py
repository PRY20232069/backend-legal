from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.profiles.interfaces.REST.controllers.profiles_controller import router
from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.model.usecases.get_profile_usecase import GetProfileUseCase
from appV2.profiles.infrastructure.dependencies.dependencies import get_get_profile_usecase
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError

@router.get(
    '',
    summary='Get profile',
    response_model=ProfileResource,
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        ProfileNotFoundError().status_code: ProfileNotFoundError().get_response_model(),
    },
)
def get_profile(
    response: Response,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    get_profile_usecase: GetProfileUseCase = Depends(get_get_profile_usecase),
):
    profile = get_profile_usecase((token, ))
    return profile