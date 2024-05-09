from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from appV1.models.bank import Bank
from sqlalchemy.exc import OperationalError

class BankRepository:

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, bank: Bank) -> Bank:
        self.session.add(bank)
        self.session.commit()
        self.session.refresh(bank)
        return bank

    def find_all(self) -> Sequence[Bank]:
        statement = select(Bank)

        try:
            result: Sequence[Bank] = self.session.execute(statement).scalars().all()
            return result
        except NoResultFound:
            return []
        except OperationalError:
            self.session.rollback()
            result: Sequence[Bank] = self.session.execute(statement).scalars().all()
            return result
    
    def find_by_name(self, name: str) -> Bank | None:
        statement = select(Bank).where(Bank.name == name)

        try:
            result: Bank = self.session.execute(statement).scalar_one()
            return result
        except NoResultFound:
            return None
        except OperationalError:
            self.session.rollback()
            result: Bank = self.session.execute(statement).scalar_one()
            return result
        
    def find_by_id(self, id: int) -> Bank | None:
        statement = select(Bank).where(Bank.id == id)

        try:
            result: Bank = self.session.execute(statement).scalar_one()
            return result
        except NoResultFound:
            return None
        except OperationalError:
            self.session.rollback()
            result: Bank = self.session.execute(statement).scalar_one()
            return result