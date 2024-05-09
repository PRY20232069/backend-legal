from typing import Sequence
from fastapi import HTTPException
from appV1.repositories.profile_repository import ProfileRepository
from appV1.resources.requests.save_profile_resource import SaveProfileResource
from appV1.resources.requests.save_user_resource import SaveUserResource
from appV1.resources.responses.authentication_response import AuthenticationResponse
from appV1.resources.responses.profile_resource import ProfileResource
from appV1.resources.responses.user_resource import UserResource

class ProfileService:
    def __init__(self, profileRepository: ProfileRepository):
        self.profileRepository = profileRepository

    def createProfile(self, saveProfileResource: SaveProfileResource, user_id) -> ProfileResource | Exception:
        existingProfile = self.profileRepository.find_by_user_id(user_id=user_id)
        if existingProfile:
            raise HTTPException(
                status_code=409,
                detail="Profile already exists"
            )
        
        profile = self.profileRepository.create(saveProfileResource.to_model(user_id=user_id))
        return profile.to_resource()
    
    def getAllProfilesByAdmin(self) -> Sequence[ProfileResource]:
        profiles = self.profileRepository.find_all()
        return [profile.to_resource() for profile in profiles]
    
    def getProfile(self, user_id) -> ProfileResource:
        profile = self.profileRepository.find_by_user_id(user_id=user_id)
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )
        return profile.to_resource()