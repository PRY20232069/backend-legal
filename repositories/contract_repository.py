from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from models.contract import Contract
from sqlalchemy.exc import OperationalError

class ContractRepository:

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, contract: Contract) -> Contract:
        self.session.add(contract)
        self.session.commit()
        self.session.refresh(contract)
        return contract
    
    def find_all(self) -> Sequence[Contract]:
        statement = select(Contract)

        try:
            result: Sequence[Contract] = self.session.execute(statement).scalars().all()
            return result
        except NoResultFound:
            return []
        except OperationalError:
            self.session.rollback()
            result: Sequence[Contract] = self.session.execute(statement).scalars().all()
            return result

    def find_all_by_profile_id(self, profile_id: int) -> Sequence[Contract]:
        statement = select(Contract).filter_by(profile_id=profile_id)

        try:
            result: Sequence[Contract] = self.session.execute(statement).scalars().all()
            return result
        except NoResultFound:
            return []
        except OperationalError:
            self.session.rollback()
            result: Sequence[Contract] = self.session.execute(statement).scalars().all()
            return result
        
    def find_all_by_name_and_profile_id(self, name: str, profile_id: int) -> Sequence[Contract]:
        statement = select(Contract).filter(Contract.name.contains(name), Contract.profile_id == profile_id)

        try:
            result: Sequence[Contract] = self.session.execute(statement).scalars().all()
            return result
        except NoResultFound:
            return []
        except OperationalError:
            self.session.rollback()
            result: Sequence[Contract] = self.session.execute(statement).scalars().all()
            return result
        
    def find_by_contract_id_and_profile_id(self, contract_id: int, profile_id: int) -> Contract | None:
        statement = select(Contract).filter_by(id=contract_id, profile_id=profile_id)

        try:
            result: Contract = self.session.execute(statement).scalar_one()
            return result
        except NoResultFound:
            return None
        except OperationalError:
            self.session.rollback()
            result: Contract = self.session.execute(statement).scalar_one()
            return result
        
    def find_by_name_and_profile_id(self, name: str, profile_id: int) -> Contract | None:
        statement = select(Contract).filter_by(name=name, profile_id=profile_id)

        try:
            result: Contract = self.session.execute(statement).scalar_one()
            return result
        except NoResultFound:
            return None
        except OperationalError:
            self.session.rollback()
            result: Contract = self.session.execute(statement).scalar_one()
            return result
        