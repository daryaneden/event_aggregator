import pytest

from app.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.infrastructure.database.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository
from app.infrastructure.database.repositories.sqlalchemy_sync_state_repository import SqlAlchemySyncStateRepository

def test_unit_of_work_provides_repositories(
    test_session,
    event_repository,
    sync_state_repository,
):
    uow = SqlAlchemyUnitOfWork(
        test_session,
        event_repository,
        sync_state_repository,
    )

    assert uow.event_repository is event_repository
    assert uow.sync_state_repository is sync_state_repository