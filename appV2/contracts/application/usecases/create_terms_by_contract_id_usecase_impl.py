from typing import Tuple, List
from fastapi import UploadFile
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2._shared.application.exceptions.app_exceptions import TokenInvalidError
from appV2.contracts.interfaces.REST.resources.term_resource import TermResource
from appV2.contracts.domain.model.entities.term import Term
from appV2.contracts.domain.repositories.term_repository import TermRepository
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.contracts.domain.model.usecases.create_terms_by_contract_id_usecase import CreateTermsByContractIdUseCase
from appV2.contracts.application.exceptions.contract_exceptions import ContractNotFoundError
from appV2.contracts.domain.services.document_processor_service import DocumentProcessorService
from appV2.contracts.domain.services.term_interpretation_generator_service import TermInterpretationGeneratorService
from appV2.contracts.domain.services.consumer_protection_law_matcher_service import ConsumerProtectionLawMatcherService
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository

from utils.jwt_utils import JwtUtils
from settings import NUMBER_OF_TERMS_PROCESSED_IN_PARALLEL

class CreateTermsByContractIdUseCaseImpl(CreateTermsByContractIdUseCase):

    def __init__(
        self, unit_of_work: UnitOfWork,
        term_repository: TermRepository,
        contract_repository: ContractRepository,
        profile_repository: ProfileRepository,
        document_processor_service: DocumentProcessorService,
        term_interpretation_generator_service: TermInterpretationGeneratorService,
        consumer_protection_law_matcher_service: ConsumerProtectionLawMatcherService,
    ):
        self.unit_of_work = unit_of_work
        self.term_repository = term_repository
        self.contract_repository = contract_repository
        self.profile_repository = profile_repository
        self.document_processor_service = document_processor_service
        self.term_interpretation_generator_service = term_interpretation_generator_service
        self.consumer_protection_law_matcher_service = consumer_protection_law_matcher_service

    def __call__(self, args: Tuple[Tuple[HTTPAuthorizationCredentials, int], UploadFile]) -> List[TermResource]:
        identifiers, contract_file = args
        token, contract_id = identifiers

        if not JwtUtils.is_valid(token):
            raise TokenInvalidError()

        user_id = JwtUtils.get_user_id(token)

        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile is None:
            raise ProfileNotFoundError()

        existing_contract = self.contract_repository.find_by_id_and_profile_id(contract_id, existing_profile.id)
        if existing_contract is None:
            raise ContractNotFoundError()

        contract_paragraphs = self.document_processor_service.split_paragraphs(contract_file)

        created_terms = []
        for i in range(0, len(contract_paragraphs), NUMBER_OF_TERMS_PROCESSED_IN_PARALLEL):
            contract_paragraphs_slice = contract_paragraphs[i:i+NUMBER_OF_TERMS_PROCESSED_IN_PARALLEL]

            contract_interpretations = self.term_interpretation_generator_service.generate(contract_paragraphs_slice)
            contract_laws = self.consumer_protection_law_matcher_service.match(contract_paragraphs_slice)

            for j in range(len(contract_paragraphs_slice)):
                abusive, interpretation = contract_interpretations[j]

                term = Term(
                    id=None,
                    description=contract_paragraphs_slice[j],
                    interpretation=interpretation,
                    consumer_protection_law=contract_laws[j],
                    abusive=abusive,                    
                    contract_id=contract_id
                )

                try:
                    self.term_repository.create(term)
                    self.unit_of_work.commit()
                    created_terms.append(term)
                except Exception as _e:
                    self.unit_of_work.rollback()
                    raise CreateTermError()

        return [TermResource.from_entity(term) for term in created_terms]