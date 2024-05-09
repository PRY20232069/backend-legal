from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy import String, Column, Integer
from appV1.models.base.base_entity import Base
from appV1.resources.responses.bank_resource import BankResource
from utils.constants import MAX_CHARS_ONE_LINE


class Bank(Base):
    __tablename__ = 'banks'

    id: Mapped[int] | int = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] | str = Column(String(MAX_CHARS_ONE_LINE), nullable=False)

    def to_resource(self, contracts_count: int = 0) -> BankResource:
        return BankResource(
            id=self.id,
            name=self.name,
            contracts_count=contracts_count
        )