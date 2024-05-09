from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# _T = TypeVar('_T')


class UnitOfWork(ABC):

    # repository: _T

    @abstractmethod
    def begin(self):
        raise NotImplementedError()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()