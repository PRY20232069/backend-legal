from typing import Sequence
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from appV1.repositories.configuration.database import SessionLocal
from appV1.repositories.profile_repository import ProfileRepository
from appV1.resources.requests.save_profile_resource import SaveProfileResource
from appV1.resources.responses.profile_resource import ProfileResource
from appV1.services.profile_service import ProfileService
from utils.jwt_utils import JwtUtils

profiles_router = APIRouter(
    prefix='/api/v1/profiles',
    tags=['Profiles'],
)

router = profiles_router

profileSession = SessionLocal()
profileRepository = ProfileRepository(profileSession)
profileService = ProfileService(profileRepository)

bearer_scheme = HTTPBearer()

@router.post("")
def create_profile(saveProfileResource: SaveProfileResource, token: str = Depends(bearer_scheme)) -> ProfileResource:
    user_id = JwtUtils.getUserId(token=token)
    profileResource = profileService.createProfile(saveProfileResource=saveProfileResource, user_id=user_id)
    return profileResource

@router.get("/admin")
def get_all_profiles_only_admin() -> Sequence[ProfileResource]:
    profileResources = profileService.getAllProfilesByAdmin()
    return profileResources

@router.get("")
def get_profile(token: str = Depends(bearer_scheme)) -> ProfileResource:
    user_id = JwtUtils.getUserId(token=token)
    profileResource = profileService.getProfile(user_id=user_id)
    return profileResource