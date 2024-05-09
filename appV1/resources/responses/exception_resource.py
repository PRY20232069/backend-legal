from pydantic import BaseModel

class ExceptionResource(BaseModel):
    message: str