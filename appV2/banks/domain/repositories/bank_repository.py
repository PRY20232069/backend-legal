from abc import abstractmethod

from appV2._shared.domain.repositories.base_repository import BaseRepository
from appV2.banks.domain.model.entities.bank import Bank


class BankRepository(BaseRepository[Bank]):
    
    @abstractmethod
    def find_by_name(self, name: str) -> Bank | None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_contracts_count_by_bank_id(self, id: int) -> int:
        raise NotImplementedError()