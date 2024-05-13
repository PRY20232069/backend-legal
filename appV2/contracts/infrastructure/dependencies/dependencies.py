from fastapi import Depends
from sqlalchemy.orm import Session

from appV2._shared.infrastructure.configuration.database import get_session
from appV2._shared.infrastructure.dependencies.dependencies import get_unit_of_work
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.contracts.infrastructure.repositories.contract_repository_impl import ContractRepositoryImpl
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.contracts.application.usecases.upload_contract_usecase_impl import UploadContractUseCaseImpl
from appV2.contracts.domain.model.usecases.upload_contract_usecase import UploadContractUseCase
from appV2.contracts.application.usecases.get_all_contracts_usecase_impl import GetAllContractsUseCaseImpl
from appV2.contracts.domain.model.usecases.get_all_contracts_usecase import GetAllContractsUseCase
from appV2.contracts.application.usecases.get_contract_by_id_usecase_impl import GetContractByIdUseCaseImpl
from appV2.contracts.domain.model.usecases.get_contract_by_id_usecase import GetContractByIdUseCase
from appV2.profiles.infrastructure.dependencies.dependencies import get_profile_repository
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository


def get_contract_repository(session: Session = Depends(get_session)) -> ContractRepository:
    return ContractRepositoryImpl(session)

def get_upload_contract_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    contract_repository: ContractRepository = Depends(get_contract_repository),
    profile_repository: ProfileRepository = Depends(get_profile_repository)
) -> UploadContractUseCase:
    return UploadContractUseCaseImpl(
        unit_of_work, 
        contract_repository,
        profile_repository
    )

def get_get_all_contracts_by_user_id_usecase(
    contract_repository: ContractRepository = Depends(get_contract_repository),
    profile_repository: ProfileRepository = Depends(get_profile_repository)
) -> GetAllContractsUseCase:
    return GetAllContractsUseCaseImpl(
        contract_repository,
        profile_repository
    )

def get_get_contract_by_id_usecase(
    contract_repository: ContractRepository = Depends(get_contract_repository),
    profile_repository: ProfileRepository = Depends(get_profile_repository)
) -> GetContractByIdUseCase:
    return GetContractByIdUseCaseImpl(
        contract_repository,
        profile_repository
    )