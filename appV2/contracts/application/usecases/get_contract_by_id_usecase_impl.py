from typing import Tuple

from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.contracts.domain.model.usecases.get_contract_by_id_usecase import GetContractByIdUseCase
from appV2.contracts.application.exceptions.contract_exceptions import ContractNotFoundError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository

from utils.jwt_utils import JwtUtils

class GetContractByIdUseCaseImpl(GetContractByIdUseCase):

    def __init__(
        self, contract_repository: ContractRepository,
        profile_repository: ProfileRepository
    ):
        self.contract_repository = contract_repository
        self.profile_repository = profile_repository

    def __call__(self, args: Tuple[str, int]) -> ContractResource:
        token, contract_id = args
        user_id = JwtUtils.getUserId(token)

        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile is None:
            raise ProfileNotFoundError()

        existing_contract = self.contract_repository.find_by_id_and_profile_id(contract_id, existing_profile.id)
        if existing_contract is None:
            raise ContractNotFoundError()

        return ContractResource.from_entity(existing_contract)