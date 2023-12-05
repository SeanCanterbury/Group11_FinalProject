from fastapi.testclient import TestClient
from ..controllers import ratings as controller
from ..main import app
import pytest
from ..models import ratings as resModel
from unittest.mock import Mock


# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_rating(db_session):
    rating_data = {
        "customer_name": "Sean",
        "rating": 10,
        "description": "great service"
    }

    rating_object = resModel.Rating(**rating_data)
    
    # Call the create function
    created_rating = controller.create(db_session, rating_object)

    # Assertions
    assert created_rating.customer_name == rating_object.customer_name
    assert created_rating.rating == rating_object.rating
    assert created_rating.description == rating_object.description
    

def test_create_rating_above_10(db_session):
    rating_data = {
        "customer_name": "Sean",
        "rating": 15,
        "description": "great service"
    }

    rating_object = resModel.Rating(**rating_data)
    
    # Call the create function
    created_rating = controller.create(db_session, rating_object)

    # Assertions
    assert created_rating.customer_name == rating_object.customer_name
    assert created_rating.rating == 10
    assert created_rating.description == rating_object.description
    

def test_create_rating_below_1(db_session):
    rating_data = {
        "customer_name": "Sean",
        "rating": -15,
        "description": "great service"
    }

    rating_object = resModel.Rating(**rating_data)
    
    # Call the create function
    created_rating = controller.create(db_session, rating_object)

    # Assertions
    assert created_rating.customer_name == rating_object.customer_name
    assert created_rating.rating == 1
    assert created_rating.description == rating_object.description