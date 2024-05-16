from pydantic import BaseModel, Field

class SaveBankResource(BaseModel):
    name: str = Field(example='BCP')
    logo_url: str = Field(example='https://bcp_logo.com.png')
