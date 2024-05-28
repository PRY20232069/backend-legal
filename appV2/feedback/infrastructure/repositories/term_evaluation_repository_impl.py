from typing import Sequence, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, update, delete, func

from appV2.feedback.domain.repositories.term_evaluation_repository import TermEvaluationRepository
from appV2.feedback.domain.model.entities.term_evaluation import TermEvaluation


class TermEvaluationRepositoryImpl(TermEvaluationRepository):
    def __init__(self, session: Session):
        super().__init__(session)
        
    def find_by_term_id_and_profile_id(self, term_id: int, profile_id: int) -> TermEvaluation | None:
        try:
            return self.session.query(TermEvaluation).filter_by(term_id=term_id, profile_id=profile_id).one()
        except NoResultFound:
            return None
            

    def findall(self) -> Sequence[TermEvaluation]:
        statement = select(TermEvaluation)
        try:
            return self.session.execute(statement).scalars().all()
        except NoResultFound:
            return []
            

    def delete_by_id(self, id_: int) -> TermEvaluation:
        statement = delete(TermEvaluation).where(TermEvaluation.id == id_)
        self.session.execute(statement)
        return True