from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from models.term import Term

class TermRepository:

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, term: Term) -> Term:
        self.session.add(term)
        self.session.commit()
        self.session.refresh(term)
        return term
    
    def update(self, term: Term) -> Term:
        self.session.commit()
        self.session.refresh(term)
        return term

    def find_all(self) -> Sequence[Term]:
        statement = select(Term)

        try:
            result: Sequence[Term] = self.session.execute(statement).scalars().all()
            return result
        except NoResultFound:
            return []
        
    def find_all_by_contract_id(self, contract_id: int) -> Sequence[Term]:
        statement = select(Term).filter_by(contract_id=contract_id)

        try:
            result: Sequence[Term] = self.session.execute(statement).scalars().all()
            return result
        except NoResultFound:
            return []
        
    def find_by_term_id_and_contract_id(self, term_id: int, contract_id: int) -> Term | None:
        statement = select(Term).filter_by(id=term_id, contract_id=contract_id)

        try:
            result: Term = self.session.execute(statement).scalar_one()
            return result
        except NoResultFound:
            return None