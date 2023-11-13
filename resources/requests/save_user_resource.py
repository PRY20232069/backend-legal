from pydantic import BaseModel

from models.user import User

class SaveUserResource(BaseModel):
    email: str
    password: str

    def to_model(self) -> User:
        return User(
            email=self.email,
            password=self.password,
        )