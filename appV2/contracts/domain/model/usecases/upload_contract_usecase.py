from abc import abstractmethod
from typing import Tuple
from fastapi import UploadFile

from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.contracts.interfaces.REST.resources.save_contract_resource import SaveContractResource
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.contracts.domain.repositories.term_repository import TermRepository
from appV2.contracts.domain.services.pdf_validator_service import PdfValidatorService
from appV2.contracts.domain.services.firebase_storage_service import FirebaseStorageService
from appV2.contracts.domain.services.document_processor_service import DocumentProcessorService
from appV2.contracts.domain.services.term_interpretation_generator_service import TermInterpretationGeneratorService
from appV2.contracts.domain.services.consumer_protection_law_matcher_service import ConsumerProtectionLawMatcherService
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.banks.domain.repositories.bank_repository import BankRepository


class UploadContractUseCase(BaseUseCase[Tuple[Tuple[str, int], UploadFile], ContractResource]):

    unit_of_work: UnitOfWork
    contract_repository: ContractRepository
    profile_repository: ProfileRepository
    bank_repository: BankRepository
    term_repository: TermRepository
    pdf_validator_service: PdfValidatorService
    firebase_storage_service: FirebaseStorageService
    document_processor_service: DocumentProcessorService
    term_interpretation_generator_service: TermInterpretationGeneratorService
    consumer_protection_law_matcher_service: ConsumerProtectionLawMatcherService

    @abstractmethod
    def __call__(self, args: Tuple[Tuple[str, int], UploadFile]) -> ContractResource:
        raise NotImplementedError()