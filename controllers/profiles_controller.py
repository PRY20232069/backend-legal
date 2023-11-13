from typing import Sequence
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from repositories.configuration.database import SessionLocal
from repositories.profile_repository import ProfileRepository
from resources.requests.save_profile_resource import SaveProfileResource
from resources.responses.profile_resource import ProfileResource
from services.profile_service import ProfileService
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

@router.post("/")
def create_profile(saveProfileResource: SaveProfileResource, token: str = Depends(bearer_scheme)) -> ProfileResource:
    user_id = JwtUtils.getUserId(token=token)
    profileResource = profileService.createProfile(saveProfileResource=saveProfileResource, user_id=user_id)
    return profileResource

@router.get("/admin")
def get_all_profiles_by_admin() -> Sequence[ProfileResource]:
    profileResources = profileService.getAllProfilesByAdmin()
    return profileResources

@router.get("/")
def get_profile(token: str = Depends(bearer_scheme)) -> ProfileResource:
    user_id = JwtUtils.getUserId(token=token)
    profileResource = profileService.getProfile(user_id=user_id)
    return profileResource