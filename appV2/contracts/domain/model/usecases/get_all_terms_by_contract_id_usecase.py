from abc import abstractmethod
from typing import Tuple, List
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2.contracts.interfaces.REST.resources.term_resource import TermResource
from appV2.contracts.domain.repositories.term_repository import TermRepository
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository


class GetAllTermsByContractIdUseCase(BaseUseCase[Tuple[HTTPAuthorizationCredentials, int], List[TermResource]]):

    term_repository: TermRepository
    contract_repository: ContractRepository
    profile_repository: ProfileRepository

    @abstractmethod
    def __call__(self, args: Tuple[HTTPAuthorizationCredentials, int]) -> List[TermResource]:
        raise NotImplementedError()