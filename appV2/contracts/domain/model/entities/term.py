from appV1.models.base.base_entity import Base
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean

from appV2._shared.domain.model.entities.base_entity import Base

from utils.constants import MAX_CHARS_MULTI_LINE

class Term(Base):
    __tablename__ = 'terms'

    id: Mapped[int] | int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description: Mapped[str] | str = Column(Text, nullable=False)
    interpretation: Mapped[str] | str | None = Column(Text, nullable=True)
    consumer_protection_law: Mapped[str] | str | None = Column(Text, nullable=True)
    abusive: Mapped[bool] | bool = Column(Boolean, default=False, nullable=False)
    contract_id: Mapped[int] | int = Column(Integer, ForeignKey('contracts.id'), nullable=False)