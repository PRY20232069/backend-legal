from abc import abstractmethod
from typing import List
from sqlalchemy.orm import Session

from appV2.contracts.domain.model.entities.term import Term
from appV2.contracts.domain.repositories.term_repository import TermRepository
from appV2.feedback.domain.model.entities.term_evaluation import TermEvaluation


class TermRepositoryImpl(TermRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_by_id(self, id: int) -> Term | None:
        result: Term | None = self.session.get(Term, id)
        return result
    
    def findall_by_contract_id(self, contract_id: int) -> List[Term]:
        return self.session.query(Term).filter(Term.contract_id == contract_id).all()

    def find_term_evaluation_by_term_id_and_profile_id(self, term_id: int, profile_id: int) -> TermEvaluation | None:
        return self.session.query(TermEvaluation).filter(TermEvaluation.term_id == term_id, TermEvaluation.profile_id == profile_id).first()