from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from typing import Sequence

from appV2.contracts.domain.model.entities.contract import Contract
from appV2.contracts.domain.repositories.contract_repository import ContractRepository


class ContractRepositoryImpl(ContractRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_by_name_and_profile_id(self, name: str, profile_id: int) -> Contract | None:
        try:
            result = self.session.query(Contract).filter(Contract.name == name, Contract.profile_id == profile_id).one()
            return result
        except NoResultFound:
            result = None
        return result

    def findall_by_profile_id(self, profile_id: int) -> list[Contract]:
        return self.session.query(Contract).filter(Contract.profile_id == profile_id).all()

    def find_by_id_and_profile_id(self, contract_id: int, profile_id: int) -> Contract | None:
        try:
            result = self.session.query(Contract).filter(Contract.id == contract_id, Contract.profile_id == profile_id).one()
            return result
        except NoResultFound:
            result = None
        return result