from fastapi import Depends, HTTPException, status, Response, Request, APIRouter

from appV2.users.interfaces.REST.controllers.users_controller import router
from appV2.users.interfaces.REST.resources.recover_user_resource import RecoverUserResource
from appV2.users.interfaces.REST.resources.user_resource import UserResource
from appV2.users.domain.model.usecases.recover_user_usecase import RecoverUserUseCase
from appV2.users.infrastructure.dependencies.dependencies import get_recover_user_usecase
from appV2.users.application.exceptions.user_exceptions import UserNotFoundError, RecoverUserError

@router.post(
    '/recover',
    summary='Recover a user',
    response_model=UserResource,
    status_code=status.HTTP_200_OK,
    responses={
        UserNotFoundError().status_code: UserNotFoundError().get_response_model(),
        RecoverUserError().status_code: RecoverUserError().get_response_model(),
    },
)
def recover_user(
    data: RecoverUserResource,
    response: Response,
    request: Request,
    recover_user_usecase: RecoverUserUseCase = Depends(get_recover_user_usecase),
):
    user = recover_user_usecase((data, ))
    return user