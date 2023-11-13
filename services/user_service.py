import jwt
from typing import Sequence
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from repositories.user_repository import UserRepository
from resources.requests.save_user_resource import SaveUserResource
from resources.responses.authentication_response import AuthenticationResponse
from resources.responses.user_resource import UserResource
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

class UserService:
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository
        self.password_hasher = CryptContext(schemes=["bcrypt"])

    def createUser(self, saveUserResource: SaveUserResource) -> UserResource | Exception:
        existingUser = self.userRepository.find_by_email(email=saveUserResource.email)
        if existingUser:
            raise HTTPException(
                status_code=409,
                detail="User already exists"
            )

        saveUserResource.password = self.password_hasher.hash(saveUserResource.password)
        user = self.userRepository.create(saveUserResource.to_model())
        return user.to_resource()
    
    def loginUser(self, saveUserResource: SaveUserResource) -> AuthenticationResponse:
        existingUser = self.userRepository.find_by_email(email=saveUserResource.email)
        if not existingUser:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        if not self.password_hasher.verify(saveUserResource.password, existingUser.password):
            raise HTTPException(
                status_code=400,
                detail="Invalid credentials"
            )
        
        expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"id": existingUser.id, "exp": expiration}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return AuthenticationResponse(token=token)
    
    def getAllUsersByAdmin(self) -> Sequence[UserResource]:
        users = self.userRepository.find_all()
        return [user.to_resource() for user in users]
    
    def getUser(self, id: int) -> UserResource:
        user = self.userRepository.find_by_id(id=id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return user.to_resource()