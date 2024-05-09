import jwt
from typing import Sequence
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from appV1.repositories.user_repository import UserRepository
from appV1.resources.requests.save_user_resource import SaveUserResource
from appV1.resources.responses.authentication_response import AuthenticationResponse
from appV1.resources.responses.user_resource import UserResource
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

        token = self.__generateToken__(id=user.id)

        userResource = user.to_resource()
        userResource.token = token
        return userResource
    
    def loginUser(self, saveUserResource: SaveUserResource) -> UserResource:
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
        
        token = self.__generateToken__(id=existingUser.id)

        return UserResource(
            id=existingUser.id,
            email=existingUser.email,
            token=token
        )
    
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
    

    def __generateToken__(self, id: int) -> str:
        expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"id": id, "exp": expiration}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token