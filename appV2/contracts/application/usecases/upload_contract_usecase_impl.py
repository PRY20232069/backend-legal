import os
from typing import Tuple
from fastapi import UploadFile

from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2._shared.application.exceptions.app_exceptions import TokenInvalidError
from appV2.contracts.interfaces.REST.resources.save_contract_resource import SaveContractResource
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.model.entities.contract import Contract
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.contracts.domain.model.usecases.upload_contract_usecase import UploadContractUseCase
from appV2.contracts.application.exceptions.contract_exceptions import ContractAlreadyExistsError, UploadContractError
from appV2.contracts.application.exceptions.term_exceptions import CreateTermError
from appV2.contracts.domain.services.pdf_validator_service import PdfValidatorService
from appV2.contracts.domain.services.firebase_storage_service import FirebaseStorageService
from appV2.contracts.domain.services.document_processor_service import DocumentProcessorService
from appV2.contracts.domain.services.term_interpretation_generator_service import TermInterpretationGeneratorService
from appV2.contracts.domain.services.consumer_protection_law_matcher_service import ConsumerProtectionLawMatcherService
from appV2.contracts.domain.model.entities.term import Term
from appV2.contracts.domain.repositories.term_repository import TermRepository
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.banks.domain.repositories.bank_repository import BankRepository
from appV2.banks.application.exceptions.bank_exceptions import BankNotFoundError

from utils.jwt_utils import JwtUtils

class UploadContractUseCaseImpl(UploadContractUseCase):

    def __init__(
        self, unit_of_work: UnitOfWork, 
        contract_repository: ContractRepository,
        profile_repository: ProfileRepository,
        bank_repository: BankRepository,
        term_repository: TermRepository,
        pdf_validator_service: PdfValidatorService,
        firebase_storage_service: FirebaseStorageService,
        document_processor_service: DocumentProcessorService,
        term_interpretation_generator_service: TermInterpretationGeneratorService,
        consumer_protection_law_matcher_service: ConsumerProtectionLawMatcherService
    ):
        self.unit_of_work = unit_of_work
        self.contract_repository = contract_repository
        self.profile_repository = profile_repository
        self.bank_repository = bank_repository
        self.term_repository = term_repository
        self.pdf_validator_service = pdf_validator_service
        self.firebase_storage_service = firebase_storage_service
        self.document_processor_service = document_processor_service
        self.term_interpretation_generator_service = term_interpretation_generator_service
        self.consumer_protection_law_matcher_service = consumer_protection_law_matcher_service

    async def __call__(self, args: Tuple[Tuple[str, int], UploadFile]) -> ContractResource:
        identifiers, contract_file = args
        token, bank_id = identifiers

        if not JwtUtils.is_valid(token):
            raise TokenInvalidError()

        user_id = JwtUtils.get_user_id(token)

        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile is None:
            raise ProfileNotFoundError()

        existing_bank = self.bank_repository.find_by_id(bank_id)
        if existing_bank is None:
            raise BankNotFoundError()

        await self.pdf_validator_service.validate(contract_file)

        contract_file_name, _ = os.path.splitext(contract_file.filename)
        final_name = f'{contract_file_name}.pdf'

        existing_contract = self.contract_repository.find_by_name_and_profile_id(final_name, existing_profile.id)
        
        i = 1
        while existing_contract is not None:
            final_name = f'{contract_file_name} ({i}).pdf'
            existing_contract = self.contract_repository.find_by_name_and_profile_id(final_name, existing_profile.id)
            i += 1

        contract_file_url = self.firebase_storage_service.save(final_name, contract_file)

        contract = Contract(
            id=None,
            name=final_name,
            favorite=False,
            file_url=contract_file_url,
            profile_id=existing_profile.id,
            bank_id=bank_id
        )

        try:
            self.contract_repository.create(contract)
            self.unit_of_work.commit()
        except Exception as _e:
            self.unit_of_work.rollback()
            raise UploadContractError()

        created_contract = self.contract_repository.find_by_name_and_profile_id(contract.name, contract.profile_id)

        contract_paragraphs = self.document_processor_service.split_paragraphs(contract_file)
        contract_interpretations = self.term_interpretation_generator_service.generate(contract_paragraphs)
        contract_laws = self.consumer_protection_law_matcher_service.match(contract_paragraphs)

        for i in range(len(contract_paragraphs)):
            term = Term(
                id=None,
                description=contract_paragraphs[i],
                interpretation=contract_interpretations[i],
                consumer_protection_law=contract_laws[i],
                contract_id=created_contract.id
            )

            try:
                self.term_repository.create(term)
                self.unit_of_work.commit()
            except Exception as _e:
                self.unit_of_work.rollback()
                raise CreateTermError()

        return ContractResource.from_entity(created_contract)