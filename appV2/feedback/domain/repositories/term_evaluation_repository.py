from abc import abstractmethod

from appV2._shared.domain.repositories.base_repository import BaseRepository
from appV2.feedback.domain.model.entities.term_evaluation import TermEvaluation


class TermEvaluationRepository(BaseRepository[TermEvaluation]):
    
    @abstractmethod
    def find_by_term_id_and_profile_id(self, term_id: int, profile_id: int) -> TermEvaluation | None:
        pass