from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model
from ..models import resources as resModel
from ..models import sandwiches as sandModel
from unittest.mock import Mock


# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order(db_session):
    # Create a sample order
    order_data = {
        "customer_name": "test",
        "description": "testing",
        "order_complete": False,
        "card_number": "0123 4567 8910 1112",
        "cvv": "000",
        "card_name": "string",
        "exp_month": "00",
        "exp_year": "00",
        "sandwich_id": 1,
        "amount": 2
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
    order_object = model.Order(**order_data)

    mock_sandwich = Mock()
    mock_sandwich.price = 10  # Set a valid price for the Mock sandwich

    # Mock the query method on the db_session
    db_session.query.return_value.filter.return_value.first.return_value = mock_sandwich

    # Call the create function
    created_order = controller.create(db_session, order_object)

    # Assertions
    assert created_order is not None
    assert created_order.customer_name == "test"
    assert created_order.description == "testing"
    assert created_order.card_number == "0123 4567 8910 1112"
    assert created_order.cvv == "000"
    assert created_order.card_name == "string"
    assert created_order.exp_month == "00"
    assert created_order.exp_year == "00"
    assert created_order.sandwich_id == 1
    assert created_order.amount == 2
    
    

