from pydantic import BaseModel, Field

from appV2.users.domain.model.entities.user import User

class UserResource(BaseModel):
    id: int
    email: str = Field(example='helloworld@hotmail.com')
    token: str

    @staticmethod
    def from_entity(entity: User) -> 'UserResource':
        return UserResource(
            id=entity.id,
            email=entity.email,
            token=''
        )