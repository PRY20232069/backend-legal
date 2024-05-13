from abc import abstractmethod

from appV2._shared.domain.repositories.base_repository import BaseRepository
from appV2.contracts.domain.model.entities.contract import Contract


class ContractRepository(BaseRepository[Contract]):
    
    @abstractmethod
    def find_by_name_and_profile_id(self, name: str, profile_id: int) -> Contract | None:
        raise NotImplementedError()

    @abstractmethod
    def findall_by_profile_id(self, profile_id: int) -> list[Contract]:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id_and_profile_id(self, contract_id: int, profile_id: int) -> Contract | None:
        raise NotImplementedError()