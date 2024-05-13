from typing import Tuple, List

from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.contracts.domain.model.usecases.get_all_contracts_usecase import GetAllContractsUseCase
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository

from utils.jwt_utils import JwtUtils

class GetAllContractsUseCaseImpl(GetAllContractsUseCase):

    def __init__(
        self, contract_repository: ContractRepository,
        profile_repository: ProfileRepository
    ):
        self.contract_repository = contract_repository
        self.profile_repository = profile_repository

    def __call__(self, args: Tuple[str]) -> List[ContractResource]:
        token, = args
        user_id = JwtUtils.getUserId(token)

        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile is None:
            raise ProfileNotFoundError()

        existing_contracts = self.contract_repository.findall_by_profile_id(existing_profile.id)

        return [ContractResource.from_entity(contract) for contract in existing_contracts]