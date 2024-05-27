from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import Sequence

from appV2.banks.domain.model.entities.bank import Bank
from appV2.banks.domain.repositories.bank_repository import BankRepository
from appV2.contracts.domain.model.entities.contract import Contract


class BankRepositoryImpl(BankRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_by_id(self, id: int) -> Bank | None:
        result: Bank | None = self.session.get(Bank, id)
        return result

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

    def get_contracts_count_by_bank_id(self, id: int) -> int:
        statement = select(func.count(Contract.id)).where(Contract.bank_id == id)
        result = self.session.execute(statement).scalar()
        if result is None:
            return 0
        else:
            return result

    def update(self, bank: Bank) -> Bank:
        update_data = bank.to_dict()

        statement = update(
            Bank
        ).where(
            Bank.id == bank.id
        ).values(
            update_data
        )

        self.session.execute(statement)
        return bank
            

    def delete_by_id(self, id_: int) -> Bank:
        statement = delete(Bank).where(Bank.id == id_)
        self.session.execute(statement)
        return True