from abc import abstractmethod
from typing import List

from appV2._shared.domain.repositories.base_repository import BaseRepository
from appV2.contracts.domain.model.entities.term import Term


class TermRepository(BaseRepository[Term]):

    @abstractmethod
    def findall_by_contract_id(self, contract_id: int) -> List[Term]:
        raise NotImplementedError()