from pydantic import BaseModel, Field

class SaveUserResource(BaseModel):
    email: str = Field(example='helloworld@hotmail.com')
    password: str = Field(example='password')