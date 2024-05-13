from typing import Tuple

from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.contracts.interfaces.REST.resources.save_contract_resource import SaveContractResource
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.model.entities.contract import Contract
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.contracts.domain.model.usecases.upload_contract_usecase import UploadContractUseCase
from appV2.contracts.application.exceptions.contract_exceptions import ContractAlreadyExistsError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository

from utils.jwt_utils import JwtUtils

class UploadContractUseCaseImpl(UploadContractUseCase):

    def __init__(
        self, unit_of_work: UnitOfWork, 
        contract_repository: ContractRepository,
        profile_repository: ProfileRepository
    ):
        self.unit_of_work = unit_of_work
        self.contract_repository = contract_repository
        self.profile_repository = profile_repository

    def __call__(self, args: Tuple[str, SaveContractResource]) -> ContractResource:
        token, data = args
        user_id = JwtUtils.getUserId(token)

        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile is None:
            raise ProfileNotFoundError()

        contract = Contract(
            id=None,
            **data.dict(),
            profile_id=existing_profile.id
        )

        existing_contract = self.contract_repository.find_by_name_and_profile_id(contract.name, contract.profile_id)
        if existing_contract is not None:
            raise ContractAlreadyExistsError()

        try:
            self.contract_repository.create(contract)
        except Exception as _e:
            self.unit_of_work.rollback()
            raise

        self.unit_of_work.commit()

        created_contract = self.contract_repository.find_by_name_and_profile_id(contract.name, contract.profile_id)

        return ContractResource.from_entity(created_contract)