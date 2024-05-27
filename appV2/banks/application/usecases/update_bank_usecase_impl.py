from typing import Tuple
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.banks.interfaces.REST.resources.save_bank_resource import SaveBankResource
from appV2.banks.interfaces.REST.resources.bank_resource import BankResource
from appV2.banks.domain.model.entities.bank import Bank
from appV2.banks.domain.repositories.bank_repository import BankRepository
from appV2.banks.domain.model.usecases.update_bank_usecase import UpdateBankUseCase
from appV2.banks.application.exceptions.bank_exceptions import BankNotFoundError, UpdateBankError

from utils.jwt_utils import JwtUtils

class UpdateBankUseCaseImpl(UpdateBankUseCase):

    def __init__(
        self, unit_of_work: UnitOfWork, 
        bank_repository: BankRepository
    ):
        self.unit_of_work = unit_of_work
        self.bank_repository = bank_repository

    def __call__(self, args: Tuple[Tuple[HTTPAuthorizationCredentials, int], SaveBankResource]) -> BankResource:
        identifiers, data = args
        token, bank_id = identifiers
        user_id = JwtUtils.get_user_id(token)

        existing_bank = self.bank_repository.find_by_id(bank_id)
        if existing_bank is None:
            raise BankNotFoundError()

        existing_bank.name = data.name
        existing_bank.logo_url = data.logo_url

        try:
            self.bank_repository.update(existing_bank)
            self.unit_of_work.commit()
        except Exception as _e:
            self.unit_of_work.rollback()
            raise UpdateBankError()

        updated_bank = self.bank_repository.find_by_id(bank_id)

        bank_resource = BankResource.from_entity(updated_bank)
        bank_resource.contracts_count = self.bank_repository.get_contracts_count_by_bank_id(bank_id)
        
        return bank_resource