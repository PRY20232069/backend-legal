from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey

from appV2._shared.domain.model.entities.base_entity import Base

from utils.constants import MAX_CHARS_ONE_LINE, MAX_CHARS_ONE_LINE_SUPER_SMALL

class TermEvaluation(Base):
    __tablename__ = 'term_evaluations'

    id: Mapped[int] | int = Column(Integer, primary_key=True, autoincrement=True)
    client_likes_term_interpretation: Mapped[bool] | bool | None = Column(Integer, nullable=True)
    client_likes_consumer_protection_law_matching: Mapped[bool] | bool | None = Column(Integer, nullable=True)
    updated_at: Mapped[datetime] | datetime = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    profile_id: Mapped[int] | int = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    term_id: Mapped[int] | int = Column(Integer, ForeignKey('terms.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'client_likes_term_interpretation': self.client_likes_term_interpretation,
            'client_likes_consumer_protection_law_matching': self.client_likes_consumer_protection_law_matching,
            'updated_at': self.updated_at,
            'profile_id': self.profile_id,
            'term_id': self.term_id,
        }