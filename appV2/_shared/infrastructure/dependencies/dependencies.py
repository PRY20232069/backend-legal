from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from appV2._shared.application.configuration.config import Settings
from appV2._shared.infrastructure.configuration.database import get_session
from appV2._shared.domain.repositories.unit_of_work import UnitOfWork
from appV2._shared.infrastructure.repositories.unit_of_work_impl import UnitOfWorkImpl


@lru_cache()
def get_settings():
    return Settings()


def get_unit_of_work(
    session: Session = Depends(get_session),
    # user_repository: UserRepository = Depends(get_user_repository),
) -> UnitOfWork:
    return UnitOfWorkImpl(session)