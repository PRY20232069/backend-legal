from abc import abstractmethod
from typing import Tuple

from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository


class GetContractByIdUseCase(BaseUseCase[Tuple[str, int], ContractResource]):

    contract_repository: ContractRepository
    profile_repository: ProfileRepository

    @abstractmethod
    def __call__(self, args: Tuple[str, int]) -> ContractResource:
        raise NotImplementedError()