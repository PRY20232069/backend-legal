from abc import abstractmethod
from typing import Tuple
from fastapi import UploadFile
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.contracts.interfaces.REST.resources.save_contract_resource import SaveContractResource
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.contracts.domain.services.pdf_validator_service import PdfValidatorService
from appV2.contracts.domain.services.firebase_storage_service import FirebaseStorageService
from appV2.contracts.domain.model.usecases.create_terms_by_contract_id_usecase import CreateTermsByContractIdUseCase
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.banks.domain.repositories.bank_repository import BankRepository


class UploadContractUseCase(BaseUseCase[Tuple[Tuple[HTTPAuthorizationCredentials, int], UploadFile], ContractResource]):

    unit_of_work: UnitOfWork
    contract_repository: ContractRepository
    profile_repository: ProfileRepository
    bank_repository: BankRepository
    pdf_validator_service: PdfValidatorService
    firebase_storage_service: FirebaseStorageService
    create_terms_usecase: CreateTermsByContractIdUseCase

    @abstractmethod
    def __call__(self, args: Tuple[Tuple[HTTPAuthorizationCredentials, int], UploadFile]) -> ContractResource:
        raise NotImplementedError()