from sqlalchemy.orm import Session

from appV2._shared.domain.repositories.unit_of_work import UnitOfWork

class UnitOfWorkImpl(UnitOfWork):

    # def __init__(self, session: Session, repository: TaskRepository):
    def __init__(self, session: Session):
        self.session: Session = session
        # self.repository: TaskRepository = repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()