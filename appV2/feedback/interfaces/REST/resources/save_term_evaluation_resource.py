from pydantic import BaseModel, Field

class SaveTermEvaluationResource(BaseModel):
    client_likes_term_interpretation: bool | None = Field(example=False)
    client_likes_consumer_protection_law_matching: bool | None = Field(example=False)