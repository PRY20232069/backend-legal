from appV1.models.base.base_entity import Base
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from appV1.resources.responses.term_resource import TermResource
from utils.constants import MAX_CHARS_MULTI_LINE

class Term(Base):
    __tablename__ = 'terms'

    id: Mapped[int] | int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description: Mapped[str] | str = Column(Text, nullable=False)
    interpretation: Mapped[str] | str | None = Column(Text, nullable=True)
    consumer_protection_law: Mapped[str] | str | None = Column(Text, nullable=True)
    index: Mapped[int] | int = Column(Integer, nullable=False)
    num_page: Mapped[int] | int = Column(Integer, nullable=False)
    contract_id: Mapped[int] | int = Column(Integer, ForeignKey('contracts.id'), nullable=False)

    def to_resource(self) -> TermResource:
        return TermResource(
            id=self.id,
            description=self.description,
            interpretation=self.interpretation,
            consumer_protection_law=self.consumer_protection_law,
            index=self.index,
            num_page=self.num_page,
            contract_id=self.contract_id
        )