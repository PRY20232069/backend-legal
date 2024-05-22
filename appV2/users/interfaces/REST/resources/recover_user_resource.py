from pydantic import BaseModel, Field

class RecoverUserResource(BaseModel):
    email: str = Field(example='helloworld@hotmail.com')