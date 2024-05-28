from typing import Tuple, List
from fastapi.security import HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenInvalidError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.profiles.domain.repositories.profile_repository import ProfileRepository
from appV2.contracts.interfaces.REST.resources.term_resource import TermResource
from appV2.contracts.domain.repositories.term_repository import TermRepository
from appV2.contracts.domain.repositories.contract_repository import ContractRepository
from appV2.contracts.domain.model.usecases.get_all_terms_by_contract_id_usecase import GetAllTermsByContractIdUseCase
from appV2.contracts.application.exceptions.contract_exceptions import ContractNotFoundError

from utils.jwt_utils import JwtUtils

class GetAllTermsByContractIdUseCaseImpl(GetAllTermsByContractIdUseCase):

    def __init__(
        self, term_repository: TermRepository,
        contract_repository: ContractRepository,
        profile_repository: ProfileRepository
    ):
        self.term_repository = term_repository
        self.contract_repository = contract_repository
        self.profile_repository = profile_repository

    def __call__(self, args: Tuple[HTTPAuthorizationCredentials, int]) -> List[TermResource]:
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

        existing_terms = self.term_repository.findall_by_contract_id(existing_contract.id)

        resources = []

        for term in existing_terms:
            resource = TermResource.from_entity(term)
            term_evaluation = self.term_repository.find_term_evaluation_by_term_id_and_profile_id(term.id, existing_profile.id)
            
            if term_evaluation is not None:
                resource.client_likes_term_interpretation = bool(term_evaluation.client_likes_term_interpretation) if term_evaluation.client_likes_term_interpretation is not None else None
                resource.client_likes_consumer_protection_law_matching = bool(term_evaluation.client_likes_consumer_protection_law_matching) if term_evaluation.client_likes_consumer_protection_law_matching is not None else None
                
            resources.append(resource)

        return resources