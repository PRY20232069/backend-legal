from typing import Tuple
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.banks.interfaces.REST.resources.save_bank_resource import SaveBankResource
from appV2.banks.interfaces.REST.resources.bank_resource import BankResource
from appV2.banks.domain.model.entities.bank import Bank
from appV2.banks.domain.repositories.bank_repository import BankRepository
from appV2.banks.domain.model.usecases.create_bank_usecase import CreateBankUseCase
from appV2.banks.application.exceptions.bank_exceptions import BankAlreadyExistsError, CreateBankError

from utils.jwt_utils import JwtUtils

class CreateBankUseCaseImpl(CreateBankUseCase):

    def __init__(
        self, unit_of_work: UnitOfWork, 
        bank_repository: BankRepository
    ):
        self.unit_of_work = unit_of_work
        self.bank_repository = bank_repository

    def __call__(self, args: Tuple[HTTPAuthorizationCredentials, SaveBankResource]) -> BankResource:
        token, data = args
        user_id = JwtUtils.get_user_id(token)

        bank = Bank(
            id=None,
            **data.dict()
        )

        existing_bank = self.bank_repository.find_by_name(bank.name)
        if existing_bank is not None:
            raise BankAlreadyExistsError()

        try:
            self.bank_repository.create(bank)
            self.unit_of_work.commit()
        except Exception as _e:
            self.unit_of_work.rollback()
            raise CreateBankError()

        created_bank = self.bank_repository.find_by_name(bank.name)

        bank_resource = BankResource.from_entity(created_bank)
        bank_resource.contracts_count = 0
        
        return bank_resource