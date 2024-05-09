from typing import TypeVar, Sequence, Generic

from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from abc import ABC

_T = TypeVar('_T')


class BaseRepository(ABC, Generic[_T]):

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, entity: _T) -> _T:
        self.session.add(entity)
        return entity

    def findall(self) -> Sequence[_T]:
        statement = select(_T)
        try:
            result: Sequence[_T] = self.session.execute(statement).scalars().all()
        except NoResultFound:
            return []
        return result

    def find_by_id(self, id: int) -> _T | None:
        result: _T | None = self.session.get(_T, id)
        return result

    def update(self, entity: _T) -> _T:
        statement = update(
            _T
        ).where(
            _T.id == entity.id
        ).values(
            entity
        ).returning(
            _T
        )
        enity_mapping = self.session.execute(statement).mappings().one()
        result = _T(**enity_mapping)
        return result

    def delete_by_id(self, id_: int) -> _T:
        statement = delete(
            _T
        ).filter_by(
            id=id
        ).returning(
            *_T.__table__.columns
        )
        result: User = self.session.execute(statement).scalar_one()
        return result