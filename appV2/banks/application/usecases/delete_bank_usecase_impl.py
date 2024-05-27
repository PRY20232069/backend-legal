from typing import Tuple
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.banks.interfaces.REST.resources.bank_resource import BankResource
from appV2.banks.domain.model.entities.bank import Bank
from appV2.banks.domain.repositories.bank_repository import BankRepository
from appV2.banks.domain.model.usecases.delete_bank_usecase import DeleteBankUseCase
from appV2.banks.application.exceptions.bank_exceptions import BankNotFoundError, DeleteBankError, DeleteBankWithContractsError

from utils.jwt_utils import JwtUtils

class DeleteBankUseCaseImpl(DeleteBankUseCase):

    def __init__(
        self, unit_of_work: UnitOfWork, 
        bank_repository: BankRepository
    ):
        self.unit_of_work = unit_of_work
        self.bank_repository = bank_repository

    def __call__(self, args: Tuple[HTTPAuthorizationCredentials, int]) -> BankResource:
        token, bank_id = args
        user_id = JwtUtils.get_user_id(token)

        existing_bank = self.bank_repository.find_by_id(bank_id)
        if existing_bank is None:
            raise BankNotFoundError()

        contracts_count = self.bank_repository.get_contracts_count_by_bank_id(bank_id)
        if contracts_count > 0:
            raise DeleteBankWithContractsError()

        try:
            self.bank_repository.delete_by_id(existing_bank.id)
            self.unit_of_work.commit()
        except Exception as _e:
            self.unit_of_work.rollback()
            raise DeleteBankError()

        bank_resource = BankResource.from_entity(existing_bank)
        bank_resource.contracts_count = 0
        
        return bank_resource