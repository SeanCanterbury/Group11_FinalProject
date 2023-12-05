from fastapi.testclient import TestClient
from ..controllers import promos as controller
from ..main import app
import pytest
from ..models import promos as model
from unittest.mock import Mock


# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_promo(db_session):
    promo_data = {
        "promo_code": "BOGO",
        "discount": 100,
    }

    promo_object = model.Promo(**promo_data)
    
    # Call the create function
    create_promo = controller.create(db_session, promo_object)

    # Assertions
    assert create_promo.promo_code == promo_object.promo_code
    assert create_promo.discount == promo_object.discount
