from abc import abstractmethod
from typing import Tuple

from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.banks.interfaces.REST.resources.save_bank_resource import SaveBankResource
from appV2.banks.interfaces.REST.resources.bank_resource import BankResource
from appV2.banks.domain.repositories.bank_repository import BankRepository


class CreateBankUseCase(BaseUseCase[Tuple[str, SaveBankResource], BankResource]):

    unit_of_work: UnitOfWork
    bank_repository: BankRepository

    @abstractmethod
    def __call__(self, args: Tuple[str, SaveBankResource]) -> BankResource:
        raise NotImplementedError()