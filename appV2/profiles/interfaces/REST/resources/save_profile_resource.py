from pydantic import BaseModel, Field
from datetime import datetime

class SaveProfileResource(BaseModel):
    name: str = Field(example='Juan')
    last_name: str = Field(example='Perez')
    birth_date: datetime = Field(example='1990-01-01T00:00:00')
    district: str = Field(example='San Francisco')
    region: str = Field(example='California')
    gender: str = Field(example='male')
    document_number: str = Field(example='87654321')