from pydantic import BaseModel, Field

class SaveContractResource(BaseModel):
    name: str = Field(example='Contract_Name.pdf')
    favorite: bool = Field(example=False)
    bank_id: int = Field(example=1)