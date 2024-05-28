from abc import abstractmethod
from typing import List

from appV2._shared.domain.repositories.base_repository import BaseRepository
from appV2.contracts.domain.model.entities.term import Term
from appV2.feedback.domain.model.entities.term_evaluation import TermEvaluation


class TermRepository(BaseRepository[Term]):

    @abstractmethod
    def findall_by_contract_id(self, contract_id: int) -> List[Term]:
        raise NotImplementedError()

    @abstractmethod
    def find_term_evaluation_by_term_id_and_profile_id(self, term_id: int, profile_id: int) -> TermEvaluation | None:
        raise NotImplementedError()