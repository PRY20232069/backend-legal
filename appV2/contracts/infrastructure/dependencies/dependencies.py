from fastapi import Depends
from sqlalchemy.orm import Session

from appV2._shared.infrastructure.configuration.database import get_session
from appV2._shared.infrastructure.dependencies.dependencies import get_unit_of_work
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.contracts.infrastructure.repositories.contract_repository_impl import ContractRepositoryImpl
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.contracts.infrastructure.repositories.term_repository_impl import TermRepositoryImpl
from appV2.contracts.domain.repositories.term_repository import TermRepository
from appV2.contracts.application.usecases.upload_contract_usecase_impl import UploadContractUseCaseImpl
from appV2.contracts.domain.model.usecases.upload_contract_usecase import UploadContractUseCase
from appV2.contracts.application.usecases.create_terms_by_contract_id_usecase_impl import CreateTermsByContractIdUseCaseImpl
from appV2.contracts.domain.model.usecases.create_terms_by_contract_id_usecase import CreateTermsByContractIdUseCase
from appV2.contracts.application.usecases.update_contract_usecase_impl import UpdateContractUseCaseImpl
from appV2.contracts.domain.model.usecases.update_contract_usecase import UpdateContractUseCase
from appV2.contracts.application.usecases.delete_contract_usecase_impl import DeleteContractUseCaseImpl
from appV2.contracts.domain.model.usecases.delete_contract_usecase import DeleteContractUseCase
from appV2.contracts.application.usecases.get_all_contracts_usecase_impl import GetAllContractsUseCaseImpl
from appV2.contracts.domain.model.usecases.get_all_contracts_usecase import GetAllContractsUseCase
from appV2.contracts.application.usecases.get_contract_by_id_usecase_impl import GetContractByIdUseCaseImpl
from appV2.contracts.domain.model.usecases.get_contract_by_id_usecase import GetContractByIdUseCase
from appV2.contracts.application.usecases.get_all_terms_by_contract_id_usecase_impl import GetAllTermsByContractIdUseCaseImpl
from appV2.contracts.domain.model.usecases.get_all_terms_by_contract_id_usecase import GetAllTermsByContractIdUseCase
from appV2.contracts.domain.services.pdf_validator_service import PdfValidatorService
from appV2.contracts.infrastructure.services.pdf_validator_service_impl import PdfValidatorServiceImpl
from appV2.contracts.domain.services.firebase_storage_service import FirebaseStorageService
from appV2.contracts.infrastructure.services.firebase_storage_service_impl import FirebaseStorageServiceImpl
from appV2.contracts.domain.services.document_processor_service import DocumentProcessorService
from appV2.contracts.infrastructure.services.document_processor_service_impl import DocumentProcessorServiceImpl
from appV2.contracts.domain.services.term_interpretation_generator_service import TermInterpretationGeneratorService
from appV2.contracts.infrastructure.services.term_interpretation_generator_service_impl import TermInterpretationGeneratorServiceImpl
from appV2.contracts.domain.services.consumer_protection_law_matcher_service import ConsumerProtectionLawMatcherService
from appV2.contracts.infrastructure.services.consumer_protection_law_matcher_service_impl import ConsumerProtectionLawMatcherServiceImpl
from appV2.profiles.infrastructure.dependencies.dependencies import get_profile_repository
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.banks.domain.repositories.bank_repository import BankRepository
from appV2.banks.infrastructure.dependencies.dependencies import get_bank_repository


def get_contract_repository(session: Session = Depends(get_session)) -> ContractRepository:
    return ContractRepositoryImpl(session)
    
def get_term_repository(session: Session = Depends(get_session)) -> TermRepository:
    return TermRepositoryImpl(session)

def get_pdf_validator_service() -> PdfValidatorService:
    return PdfValidatorServiceImpl()

def get_firebase_storage_service() -> FirebaseStorageService:
    return FirebaseStorageServiceImpl()

def get_document_processor_service() -> DocumentProcessorService:
    return DocumentProcessorServiceImpl()

def get_term_interpretation_generator_service() -> TermInterpretationGeneratorService:
    return TermInterpretationGeneratorServiceImpl()

def get_consumer_protection_law_matcher_service() -> ConsumerProtectionLawMatcherService:
    return ConsumerProtectionLawMatcherServiceImpl()

def get_create_terms_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    term_repository: TermRepository = Depends(get_term_repository),
    contract_repository: ContractRepository = Depends(get_contract_repository),
    profile_repository: ProfileRepository = Depends(get_profile_repository),
    document_processor_service: DocumentProcessorService = Depends(get_document_processor_service),
    term_interpretation_generator_service: TermInterpretationGeneratorService = Depends(get_term_interpretation_generator_service),
    consumer_protection_law_matcher_service: ConsumerProtectionLawMatcherService = Depends(get_consumer_protection_law_matcher_service),
) -> CreateTermsByContractIdUseCase:
    return CreateTermsByContractIdUseCaseImpl(
        unit_of_work, 
        term_repository,
        contract_repository,
        profile_repository,
        document_processor_service,
        term_interpretation_generator_service,
        consumer_protection_law_matcher_service,
    )

def get_upload_contract_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    contract_repository: ContractRepository = Depends(get_contract_repository),
    profile_repository: ProfileRepository = Depends(get_profile_repository),
    bank_repository: BankRepository = Depends(get_bank_repository),
    pdf_validator_service: PdfValidatorService = Depends(get_pdf_validator_service),
    firebase_storage_service: FirebaseStorageService = Depends(get_firebase_storage_service),
    create_terms_usecase: CreateTermsByContractIdUseCase = Depends(get_create_terms_usecase)
) -> UploadContractUseCase:
    return UploadContractUseCaseImpl(
        unit_of_work, 
        contract_repository,
        profile_repository,
        bank_repository,
        pdf_validator_service,
        firebase_storage_service,
        create_terms_usecase,
    )

def get_update_contract_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    contract_repository: ContractRepository = Depends(get_contract_repository),
    profile_repository: ProfileRepository = Depends(get_profile_repository)
) -> UpdateContractUseCase:
    return UpdateContractUseCaseImpl(
        unit_of_work, 
        contract_repository,
        profile_repository
    )

def get_delete_contract_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    contract_repository: ContractRepository = Depends(get_contract_repository),
    profile_repository: ProfileRepository = Depends(get_profile_repository)
) -> DeleteContractUseCase:
    return DeleteContractUseCaseImpl(
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

def get_get_all_terms_by_contract_id_usecase(
    term_repository: TermRepository = Depends(get_term_repository),
    contract_repository: ContractRepository = Depends(get_contract_repository),
    profile_repository: ProfileRepository = Depends(get_profile_repository)
) -> GetAllTermsByContractIdUseCase:
    return GetAllTermsByContractIdUseCaseImpl(
        term_repository,
        contract_repository,
        profile_repository
    )