from fastapi.testclient import TestClient
from ..controllers import sandwiches as controller
from ..main import app
import pytest
from ..models import sandwiches as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_sandwich(db_session):
    sandwich_data = {
        "sandwich_name": "Burger",
        "price": 10
    }

    sandwich_object = model.Sandwich(**sandwich_data)

    # Call the create function
    created_sandwich = controller.create(db_session, sandwich_object)

    # Assertions
    assert created_sandwich is not None
    assert created_sandwich.sandwich_name == "Burger"
    assert created_sandwich.price == 10
