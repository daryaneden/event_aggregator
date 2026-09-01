
from app.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork

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