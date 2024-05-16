from typing import Tuple
from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2.profiles.interfaces.REST.controllers.profiles_controller import router
from appV2.profiles.interfaces.REST.resources.save_profile_resource import SaveProfileResource
from appV2.profiles.interfaces.REST.resources.profile_resource import ProfileResource
from appV2.profiles.domain.model.usecases.create_profile_usecase import CreateProfileUseCase
from appV2.profiles.infrastructure.dependencies.dependencies import get_create_profile_usecase
from appV2.profiles.application.exceptions.profile_exceptions import ProfileAlreadyExistsError, CreateProfileError
from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError

@router.post(
    '',
    summary='Create a new profile',
    response_model=ProfileResource,
    status_code=status.HTTP_201_CREATED,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        ProfileAlreadyExistsError().status_code: ProfileAlreadyExistsError().get_response_model(),
        CreateProfileError().status_code: CreateProfileError().get_response_model(),
    },
)
def create_profile(
    data: SaveProfileResource,
    response: Response,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    create_profile_usecase: CreateProfileUseCase = Depends(get_create_profile_usecase),
):
    profile = create_profile_usecase((token, data))
    return profile