from abc import abstractmethod
from typing import Tuple
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository


class DeleteContractUseCase(BaseUseCase[Tuple[HTTPAuthorizationCredentials, int], ContractResource]):

    unit_of_work: UnitOfWork
    contract_repository: ContractRepository
    profile_repository: ProfileRepository

    @abstractmethod
    def __call__(self, args: Tuple[HTTPAuthorizationCredentials, int]) -> ContractResource:
        raise NotImplementedError()