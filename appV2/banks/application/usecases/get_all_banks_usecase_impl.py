from typing import Tuple, List
from fastapi.security import HTTPAuthorizationCredentials

from appV2.banks.interfaces.REST.resources.bank_resource import BankResource
from appV2.banks.domain.repositories.bank_repository import BankRepository
from appV2.banks.domain.model.usecases.get_all_banks_usecase import GetAllBanksUseCase

from utils.jwt_utils import JwtUtils

class GetAllBanksUseCaseImpl(GetAllBanksUseCase):

    def __init__(
        self, bank_repository: BankRepository
    ):
        self.bank_repository = bank_repository

    def __call__(self, args: Tuple[HTTPAuthorizationCredentials]) -> List[BankResource]:
        token, = args
        user_id = JwtUtils.get_user_id(token)

        existing_banks = self.bank_repository.findall()
        bank_resources = []

        for bank in existing_banks:
            bank_resource = BankResource.from_entity(bank)
            bank_resource.contracts_count = self.bank_repository.get_contracts_count_by_bank_id(bank.id)
            bank_resources.append(bank_resource)

        return bank_resources