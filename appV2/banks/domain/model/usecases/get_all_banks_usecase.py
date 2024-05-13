from abc import abstractmethod
from typing import Tuple, List

from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2.banks.interfaces.REST.resources.bank_resource import BankResource
from appV2.banks.domain.repositories.bank_repository import BankRepository


class GetAllBanksUseCase(BaseUseCase[str, List[BankResource]]):

    bank_repository: BankRepository

    @abstractmethod
    def __call__(self, args: Tuple[str]) -> List[BankResource]:
        raise NotImplementedError()