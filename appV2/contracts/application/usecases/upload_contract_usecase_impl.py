import os
from typing import Tuple
from fastapi import UploadFile
from fastapi.security import HTTPAuthorizationCredentials

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
from appV2.contracts.domain.repositories.term_repository import TermRepository
from appV2.contracts.domain.model.usecases.create_terms_by_contract_id_usecase import CreateTermsByContractIdUseCase
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
        pdf_validator_service: PdfValidatorService,
        firebase_storage_service: FirebaseStorageService,
        create_terms_usecase: CreateTermsByContractIdUseCase,
    ):
        self.unit_of_work = unit_of_work
        self.contract_repository = contract_repository
        self.profile_repository = profile_repository
        self.bank_repository = bank_repository
        self.pdf_validator_service = pdf_validator_service
        self.firebase_storage_service = firebase_storage_service
        self.create_terms_usecase = create_terms_usecase

    async def __call__(self, args: Tuple[Tuple[HTTPAuthorizationCredentials, int], UploadFile]) -> ContractResource:
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
            bank_id=bank_id,
            deleted=False,
        )

        try:
            self.contract_repository.create(contract)
            self.unit_of_work.commit()
        except Exception as _e:
            self.unit_of_work.rollback()
            raise UploadContractError()

        self.create_terms_usecase(((token, contract.id), contract_file))

        created_contract = self.contract_repository.find_by_name_and_profile_id(contract.name, contract.profile_id)

        resource = ContractResource.from_entity(created_contract)
        resource.terms_count = self.contract_repository.get_terms_count_by_contract_id(created_contract.id)
        resource.abusive_terms_count = self.contract_repository.get_abusive_terms_count_by_contract_id(created_contract.id)

        return resource