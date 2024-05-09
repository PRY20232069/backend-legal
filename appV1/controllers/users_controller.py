from typing import Sequence
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from appV1.repositories.configuration.database import SessionLocal
from appV1.repositories.user_repository import UserRepository
from appV1.resources.requests.save_user_resource import SaveUserResource
from appV1.resources.responses.authentication_response import AuthenticationResponse
from appV1.resources.responses.user_resource import UserResource
from appV1.services.user_service import UserService
from utils.jwt_utils import JwtUtils


users_router = APIRouter(
    prefix='/api/v1/users',
    tags=['Users'],
)

router = users_router

userSession = SessionLocal()
userRepository = UserRepository(userSession)
userService = UserService(userRepository)

bearer_scheme = HTTPBearer()

@router.post("/register")
def register_user(saveUserResource: SaveUserResource) -> UserResource:
    userResource = userService.createUser(saveUserResource=saveUserResource)
    return userResource

@router.post("/login")
def login_user(saveUserResource: SaveUserResource) -> UserResource:
    userResource = userService.loginUser(saveUserResource=saveUserResource)
    return userResource

@router.get("/admin")
def get_all_users_only_admin() -> Sequence[UserResource]:
    userResources = userService.getAllUsersByAdmin()
    return userResources

@router.get("")
def get_user(token: str = Depends(bearer_scheme)) -> UserResource:
    user_id = JwtUtils.getUserId(token=token)
    userResource = userService.getUser(id=user_id)
    return userResource