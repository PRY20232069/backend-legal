from abc import abstractmethod
from typing import Tuple, List
from fastapi import UploadFile
from fastapi.security import HTTPAuthorizationCredentials

from appV2.contracts.domain.repositories.term_repository import TermRepository
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.contracts.interfaces.REST.resources.term_resource import TermResource
from appV2.contracts.domain.services.document_processor_service import DocumentProcessorService
from appV2.contracts.domain.services.term_interpretation_generator_service import TermInterpretationGeneratorService
from appV2.contracts.domain.services.consumer_protection_law_matcher_service import ConsumerProtectionLawMatcherService
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2._shared.domain.model.usecases.base_usecase import BaseUseCase
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork


class CreateTermsByContractIdUseCase(BaseUseCase[Tuple[Tuple[HTTPAuthorizationCredentials, int], UploadFile], List[TermResource]]):

    unit_of_work: UnitOfWork
    term_repository: TermRepository
    contract_repository: ContractRepository
    profile_repository: ProfileRepository
    document_processor_service: DocumentProcessorService
    term_interpretation_generator_service: TermInterpretationGeneratorService
    consumer_protection_law_matcher_service: ConsumerProtectionLawMatcherService

    @abstractmethod
    def __call__(self, args: Tuple[Tuple[HTTPAuthorizationCredentials, int], UploadFile]) -> List[TermResource]:
        raise NotImplementedError()