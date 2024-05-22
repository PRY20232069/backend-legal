from typing import Tuple
from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2.profiles.interfaces.REST.controllers.profiles_controller import router
from appV2.profiles.interfaces.REST.resources.save_profile_resource import SaveProfileResource
from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.model.usecases.update_profile_usecase import UpdateProfileUseCase
from appV2.profiles.infrastructure.dependencies.dependencies import get_update_profile_usecase
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError, UpdateProfileError
from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError

@router.put(
    '',
    summary='Update a profile',
    response_model=ProfileResource,
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        ProfileNotFoundError().status_code: ProfileNotFoundError().get_response_model(),
        UpdateProfileError().status_code: UpdateProfileError().get_response_model(),
    },
)
def update_profile(
    data: SaveProfileResource,
    response: Response,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    update_profile_usecase: UpdateProfileUseCase = Depends(get_update_profile_usecase),
):
    profile = update_profile_usecase((token, data))
    return profile