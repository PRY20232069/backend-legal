from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from typing import Sequence

from appV2.banks.domain.model.entities.bank import Bank
from appV2.banks.domain.repositories.bank_repository import BankRepository


class BankRepositoryImpl(BankRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def findall(self) -> Sequence[Bank]:
        statement = select(Bank)
        try:
            result: Sequence[Bank] = self.session.execute(statement).scalars().all()
        except NoResultFound:
            return []
        return result

    def find_by_name(self, name: str) -> Bank | None:
        try:
            statement = select(Bank).where(Bank.name == name)
            result = self.session.execute(statement).scalars().one()
        except NoResultFound:
            result = None
        return result