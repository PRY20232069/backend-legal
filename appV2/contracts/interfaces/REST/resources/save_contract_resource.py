from pydantic import BaseModel, Field

class SaveContractResource(BaseModel):
    name: str = Field(example='Contract_Name.pdf')
    bank_id: int = Field(example=1)