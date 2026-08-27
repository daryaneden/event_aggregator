from app.application.interfaces.uow import UnitOfWork
from app.infrastructure.celery.session_factory import CelerySessionFactory
from app.infrastructure.database.repositories.sqlalchemy_sync_state_repository import SqlAlchemySyncStateRepository
from app.infrastructure.database.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository

class SqlAlchemyCeleryUnitOfWork(UnitOfWork):

    def __init__(self):
        self.session = CelerySessionFactory()

        self.event_repository = SqlAlchemyEventRepository(
            self.session
        )

        self.sync_state_repository = (
            SqlAlchemySyncStateRepository(
                self.session
            )
        )

    async def __aenter__(self):
        await self.session.begin()
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        try:
            if exc_type is not None:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()