from fastapi.testclient import TestClient
from ..controllers import recipes as controller
from ..main import app
import pytest
from ..models import recipes as model
from ..models import resources as resModel
from ..models import sandwiches as sandModel
from ..models import promos as proModel
from unittest.mock import Mock

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_recipe(db_session):
    # Create a sample recipe
    recipe_data = {
        "amount": 1,
        "sandwich_id": 1,
        "resource_id": 1
    }

    resource_data = {
        "item": "cheese",
        "amount": 10
    }

    sandwich_data = {
        "sandwich_name": "grilled cheese",
        "price": 10,  # Set a valid price for the sandwich
        "calories": 100,
        "resource_id": 1
    }

    resource_object = resModel.Resource(**resource_data)
    sandwich_object = sandModel.Sandwich(**sandwich_data)
    recipe_object = model.Recipe(**recipe_data)

    mock_sandwich = Mock()
    mock_sandwich.price = 10  # Set a valid price for the Mock sandwich

    # Mock the query method on the db_session
    db_session.query.return_value.filter.return_value.first.return_value = mock_sandwich

    # Call the create function
    created_recipe = controller.create(db_session, recipe_object)

    # Assertions
    assert created_recipe is not None
    assert created_recipe.amount == recipe_object.amount
    assert created_recipe.sandwich_id == sandwich_object.id
    assert created_recipe.resource_id == resource_object.id
