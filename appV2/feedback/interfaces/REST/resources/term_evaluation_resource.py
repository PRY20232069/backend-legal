from datetime import datetime
from pydantic import BaseModel, Field

from appV2.feedback.domain.model.entities.term_evaluation import TermEvaluation

class TermEvaluationResource(BaseModel):
    id: int = Field(example=1)
    client_likes_term_interpretation: bool | None = Field(example=False)
    client_likes_consumer_protection_law_matching: bool | None = Field(example=False)
    updated_at: datetime = Field(example=datetime.now())
    profile_id: int = Field(example=1)
    term_id: int = Field(example=1)

    @staticmethod
    def from_entity(entity: TermEvaluation) -> 'TermEvaluationResource':
        return TermEvaluationResource(
            id=entity.id,
            client_likes_term_interpretation=entity.client_likes_term_interpretation,
            client_likes_consumer_protection_law_matching=entity.client_likes_consumer_protection_law_matching,
            updated_at=entity.updated_at,
            profile_id=entity.profile_id,
            term_id=entity.term_id
        )