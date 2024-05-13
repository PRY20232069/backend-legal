from abc import abstractmethod

from appV2._shared.domain.repositories.base_repository import BaseRepository
from appV2.contracts.domain.model.entities.term import Term


class TermRepository(BaseRepository[Term]):
    pass