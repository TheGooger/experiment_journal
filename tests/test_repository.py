from datetime import datetime
import pytest
import uuid

from app.repositories.experiment_repository import ExperimentRepository
from app.schemas.experiment import ExperimentCreate, ExperimentUpdate


pytestmark = pytest.mark.asyncio


async def test_create_experiment(db_session, test_user):
    repo = ExperimentRepository()
    data = ExperimentCreate(
    experiment_number = "v260305",
    performed_at = datetime.strptime("2026-03-26", "%Y-%m-%d"),
    is_completed = False,
    project = "MAPbBr2I + Cs",
    goal = "Test experiment",
    experiment_subject = "test",
    perovskite = "MAPbBr2I",
    samples = ["1", "2", "3"],
    )

    experiment = await repo.create(db_session, data, test_user.id)
    
    assert experiment.id is not None
    assert experiment.experiment_number == "v260305"
    

async def test_read_one_not_found(db_session, test_user):
    repo = ExperimentRepository()
    result = await repo.read_one(db_session, "123", test_user.id)

    assert result is None


async def test_read_one(db_session, test_user):
    repo = ExperimentRepository()
    data = ExperimentCreate(
    experiment_number = "v260306",
    performed_at = datetime.strptime("2026-03-26", "%Y-%m-%d"),
    is_completed = False,
    project = "MAPbBr2I + Cs",
    goal = "Test experiment",
    experiment_subject = "test",
    perovskite = "MAPbBr2I",
    samples = ["1", "2", "3"],
    )
    created = await repo.create(db_session, data, test_user.id)
    found = await repo.read_one(db_session, "v260306", test_user.id)

    assert found is not None
    assert found.id == created.id


async def test_update_experiment(db_session, test_user):
    repo = ExperimentRepository()
    data = ExperimentCreate(
    experiment_number = "v260307",
    performed_at = datetime.strptime("2026-03-26", "%Y-%m-%d"),
    is_completed = False,
    project = "MAPbBr2I + Cs",
    goal = "Test experiment",
    experiment_subject = "test",
    perovskite = "MAPbBr2I",
    samples = ["1", "2", "3"],
    )
    created = await repo.create(db_session, data, test_user.id)

    update_data = ExperimentUpdate(
        is_completed=True,
    ) 
    updated = await repo.update(db_session, update_data, created.experiment_number, test_user.id)

    assert updated is not None
    assert updated.is_completed == True


async def test_update_experiment_not_found(db_session, test_user):
    repo = ExperimentRepository()
    update_data = ExperimentUpdate(
        is_completed=False,
    )
    updated = await repo.update(db_session, update_data, "123", test_user.id)

    assert updated is None


async def test_delete_experiment(db_session, test_user):
    repo = ExperimentRepository()
    data = ExperimentCreate(
    experiment_number = "v260308",
    performed_at = datetime.strptime("2026-03-26", "%Y-%m-%d"),
    is_completed = False,
    project = "MAPbBr2I + Cs",
    goal = "Test experiment",
    experiment_subject = "test",
    perovskite = "MAPbBr2I",
    samples = ["1", "2", "3"],
    )
    created = await repo.create(db_session, data, test_user.id)
    
    deleted = await repo.delete(db_session, created.experiment_number, test_user.id)

    assert deleted == True

    found = await repo.read_one(db_session, created.experiment_number, test_user.id)
    assert found is None


async def test_delete_experiment_not_found(db_session, test_user):
    repo = ExperimentRepository()

    deleted = await repo.delete(db_session, "123", test_user.id)

    assert deleted == False
