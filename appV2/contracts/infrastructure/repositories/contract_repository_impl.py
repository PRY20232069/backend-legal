from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from typing import Sequence, List

from appV2.contracts.domain.model.entities.contract import Contract
from appV2.contracts.domain.model.entities.term import Term
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

    def findall_by_profile_id(self, profile_id: int) -> List[Contract]:
        return self.session.query(Contract).filter(Contract.profile_id == profile_id).all()

    def findall_by_profile_id_and_not_deleted(self, profile_id: int) -> List[Contract]:
        return self.session.query(Contract).filter(Contract.profile_id == profile_id, Contract.deleted == False).all()

    def find_by_id_and_profile_id(self, contract_id: int, profile_id: int) -> Contract | None:
        try:
            result = self.session.query(Contract).filter(Contract.id == contract_id, Contract.profile_id == profile_id).one()
            return result
        except NoResultFound:
            result = None
        return result

    def update(self, contract: Contract) -> Contract:
        update_data = contract.to_dict()
        update_data.pop(Contract.uploaded_date.key)

        statement = update(
            Contract
        ).where(
            Contract.id == contract.id
        ).values(
            update_data
        )

        self.session.execute(statement)
        return contract
    
    def get_terms_count_by_contract_id(self, id: int) -> int:
        statement = select(func.count(Term.id)).where(Term.contract_id == id)
        result = self.session.execute(statement).scalar()
        if result is None:
            return 0
        else:
            return result
    
    def get_abusive_terms_count_by_contract_id(self, id: int) -> int:
        statement = select(func.count(Term.id)).where(Term.contract_id == id, Term.abusive == True)
        result = self.session.execute(statement).scalar()
        if result is None:
            return 0
        else:
            return result