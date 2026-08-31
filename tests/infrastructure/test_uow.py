import pytest

from app.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.infrastructure.database.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository
from app.infrastructure.database.repositories.sqlalchemy_sync_state_repository import SqlAlchemySyncStateRepository

@pytest.mark.asyncio
async def test_unit_of_work_provides_repositories(test_session):
    uow = SqlAlchemyUnitOfWork(test_session)

    assert isinstance(uow.event_repository, SqlAlchemyEventRepository)
    assert isinstance(uow.sync_state_repository, SqlAlchemySyncStateRepository)

