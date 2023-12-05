from fastapi.testclient import TestClient
from ..controllers import sandwiches as controller
from ..main import app
import pytest
from ..models import resources as resModel
from ..models import sandwiches as sandModel
from unittest.mock import Mock


# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_sandwich(db_session):
    resource_data = {
        "item": "cheese",
        "amount": 10
    }

    sandwich_data = {
        "sandwich_name": "grilled cheese",
        "price": 10,  # Set a valid price for the sandwich
        "calories": 100,
        "resource_id": 1,
        "amount": 10
    }

    resource_object = resModel.Resource(**resource_data)
    sandwich_object = sandModel.Sandwich(**sandwich_data)
    mock_resource = Mock()
    mock_resource.amount = 10  # Set a valid price for the Mock sandwich

    # Mock the query method on the db_session
    db_session.query.return_value.filter.return_value.first.return_value = mock_resource

    # Call the create function
    created_sandwich = controller.create(db_session, sandwich_object)

    # Assertions
    assert created_sandwich.sandwich_name == sandwich_object.sandwich_name
    assert created_sandwich.price == sandwich_object.price
    assert created_sandwich.calories == sandwich_object.calories
    assert created_sandwich.resource_id == sandwich_object.resource_id
    assert created_sandwich.amount == sandwich_object.amount
    