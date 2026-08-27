import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

# Snapshot of the seed data, taken before any test mutates the shared dict.
_original_activities = copy.deepcopy(activities)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    # Mutate in place so route handlers (which hold a reference to this dict) see the reset.
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))
    yield
