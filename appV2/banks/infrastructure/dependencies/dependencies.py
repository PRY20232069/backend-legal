from fastapi import Depends
from sqlalchemy.orm import Session

from appV2._shared.infrastructure.configuration.database import get_session
from appV2._shared.infrastructure.dependencies.dependencies import get_unit_of_work
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2.banks.infrastructure.repositories.bank_repository_impl import BankRepositoryImpl
from appV2.banks.domain.repositories.bank_repository import BankRepository
from appV2.banks.application.usecases.create_bank_usecase_impl import CreateBankUseCaseImpl
from appV2.banks.domain.model.usecases.create_bank_usecase import CreateBankUseCase
from appV2.banks.application.usecases.update_bank_usecase_impl import UpdateBankUseCaseImpl
from appV2.banks.domain.model.usecases.update_bank_usecase import UpdateBankUseCase
from appV2.banks.application.usecases.delete_bank_usecase_impl import DeleteBankUseCaseImpl
from appV2.banks.domain.model.usecases.delete_bank_usecase import DeleteBankUseCase
from appV2.banks.application.usecases.get_all_banks_usecase_impl import GetAllBanksUseCaseImpl
from appV2.banks.domain.model.usecases.get_all_banks_usecase import GetAllBanksUseCase


def get_bank_repository(session: Session = Depends(get_session)) -> BankRepository:
    return BankRepositoryImpl(session)

def get_create_bank_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    bank_repository: BankRepository = Depends(get_bank_repository)
) -> CreateBankUseCaseImpl:
    return CreateBankUseCaseImpl(
        unit_of_work, 
        bank_repository
    )

def get_update_bank_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    bank_repository: BankRepository = Depends(get_bank_repository)
) -> UpdateBankUseCaseImpl:
    return UpdateBankUseCaseImpl(
        unit_of_work, 
        bank_repository
    )

def get_delete_bank_usecase(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    bank_repository: BankRepository = Depends(get_bank_repository)
) -> DeleteBankUseCaseImpl:
    return DeleteBankUseCaseImpl(
        unit_of_work, 
        bank_repository
    )

def get_get_all_banks_usecase(
    bank_repository: BankRepository = Depends(get_bank_repository)
) -> GetAllBanksUseCase:
    return GetAllBanksUseCaseImpl(
        bank_repository
    )