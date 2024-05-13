from pydantic import BaseModel, Field

class SaveBankResource(BaseModel):
    name: str = Field(example='BCP')
