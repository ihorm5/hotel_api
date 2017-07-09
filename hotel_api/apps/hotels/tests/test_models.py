import pytest

from hotel_api.contrib.db import session

from hotel_api.apps.hotels.models import Hotel


@pytest.mark.gen_test
def test_customer_create(db):
    hotel = Hotel(title='Resort Hotel')
    hotel.save()

    assert hotel.id == 1
