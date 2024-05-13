from typing import Tuple, List

from appV2.banks.interfaces.REST.resources.bank_resource import BankResource
from appV2.banks.domain.repositories.bank_repository import BankRepository
from appV2.banks.domain.model.usecases.get_all_banks_usecase import GetAllBanksUseCase

from utils.jwt_utils import JwtUtils

class GetAllBanksUseCaseImpl(GetAllBanksUseCase):

    def __init__(
        self, bank_repository: BankRepository
    ):
        self.bank_repository = bank_repository

    def __call__(self, args: Tuple[str]) -> List[BankResource]:
        token, = args
        user_id = JwtUtils.getUserId(token)

        existing_banks = self.bank_repository.findall()

        return [BankResource.from_entity(bank) for bank in existing_banks]