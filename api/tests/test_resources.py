from fastapi.testclient import TestClient
from ..controllers import resources as controller
from ..main import app
import pytest
from ..models import resources as resModel
from unittest.mock import Mock


# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_resource(db_session):
    resource_data = {
        "item": "cheese",
        "amount": 10
    }


    resource_object = resModel.Resource(**resource_data)
    created_resource = controller.create(db_session, resource_object)

    # Assertions
    assert created_resource.item == resource_object.item
    assert created_resource.amount == resource_object.amount
    
    