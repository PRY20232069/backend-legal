from typing import Tuple
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.model.entities.contract import Contract
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.contracts.domain.model.usecases.delete_contract_usecase import DeleteContractUseCase
from appV2.contracts.application.exceptions.contract_exceptions import ContractNotFoundError, DeleteContractError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2._shared.application.exceptions.app_exceptions import TokenInvalidError

from utils.jwt_utils import JwtUtils

class DeleteContractUseCaseImpl(DeleteContractUseCase):

    def __init__(
        self, unit_of_work: UnitOfWork, 
        contract_repository: ContractRepository,
        profile_repository: ProfileRepository
    ):
        self.unit_of_work = unit_of_work
        self.contract_repository = contract_repository
        self.profile_repository = profile_repository

    def __call__(self, args: Tuple[HTTPAuthorizationCredentials, int]) -> ContractResource:
        token, contract_id = args

        if not JwtUtils.is_valid(token):
            raise TokenInvalidError()

        user_id = JwtUtils.get_user_id(token)

        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile is None:
            raise ProfileNotFoundError()

        existing_contract = self.contract_repository.find_by_id_and_profile_id(contract_id, existing_profile.id)
        if existing_contract is None:
            raise ContractNotFoundError()

        existing_contract.deleted = True

        try:
            self.contract_repository.update(existing_contract)
            self.unit_of_work.commit()
        except Exception as _e:
            self.unit_of_work.rollback()
            raise UpdateContractError()

        deleted_contract = self.contract_repository.find_by_name_and_profile_id(existing_contract.name, existing_contract.profile_id)

        resource = ContractResource.from_entity(deleted_contract)
        resource.terms_count = self.contract_repository.get_terms_count_by_contract_id(deleted_contract.id)
        resource.abusive_terms_count = self.contract_repository.get_abusive_terms_count_by_contract_id(deleted_contract.id)

        return resource