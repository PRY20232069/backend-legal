from abc import abstractmethod
from typing import List
from sqlalchemy.orm import Session

from appV2.contracts.domain.model.entities.term import Term
from appV2.contracts.domain.repositories.term_repository import TermRepository


class TermRepositoryImpl(TermRepository):
    def __init__(self, session: Session):
        super().__init__(session)
    
    def findall_by_contract_id(self, contract_id: int) -> List[Term]:
        return self.session.query(Term).filter(Term.contract_id == contract_id).all()