from pydantic import BaseModel

class GetTermsRequest(BaseModel):
    text: str