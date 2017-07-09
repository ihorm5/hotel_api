import json

import pytest

from hotel_api.apps.hotels.models import Hotel, HotelRoom, Client

from hotel_api.contrib.db import session


@pytest.fixture
def hotel_mock_data(mixer):
    mixer.cycle(4).blend(Hotel)
    mixer.cycle(4).blend(Client)
    mixer.cycle(4).blend(HotelRoom)


@pytest.mark.gen_test
def test_hotels_list(hotel_mock_data, http_client, base_url):
    resp = yield http_client.fetch('{}/{}'.format(base_url, 'hotels'))

    assert resp.code == 200


@pytest.mark.gen_test
def test_hotels_create(hotel_mock_data, http_client, base_url):
    resp = yield http_client.fetch('{}/{}'.format(base_url, 'hotels'),
                                   raise_error=False,
                                   method='POST',
                                   body=json.dumps({
                                       'title': 'Kiev Resort'
                                   }))
    assert resp.reason == 'Created'
    assert resp.code == 201


@pytest.mark.gen_test
def test_hotels_create_with_wrong_data(hotel_mock_data, http_client, base_url):
    resp = yield http_client.fetch('{}/{}'.format(base_url, 'hotels'),
                                   method='POST',
                                   raise_error=False,
                                   body=json.dumps({
                                       'titl1': 'Kiev Resort'
                                   }))
    assert resp.code == 400


@pytest.mark.gen_test
def test_hotels_detail(hotel_mock_data, http_client, base_url):
    resp = yield http_client.fetch(
        '{}/{}/{}'.format(base_url, 'hotels', 1)
    )

    assert resp.code == 200


@pytest.mark.gen_test
def test_adds_room_to_hotel(hotel_mock_data, http_client, base_url):
    resp = yield http_client.fetch('{}/{}'.format(base_url, 'hotel-rooms'),
                                   method='POST',
                                   raise_error=False,
                                   body=json.dumps({
                                       'hotel_id': 1,
                                       'room_id': 1
                                   }))

    assert resp.code == 201
    hotel = session.query(Hotel).get(1)
    assert len(hotel.rooms) == 1


@pytest.mark.gen_test
def test_adds_room_to_hotel_with_bad_room_id(hotel_mock_data, http_client,
                                             base_url):
    resp = yield http_client.fetch('{}/{}'.format(base_url, 'hotel-rooms'),
                                   method='POST',
                                   raise_error=False,
                                   body=json.dumps({
                                       'hotel_id': 1,
                                       'room_id': 5
                                   }))

    assert resp.code == 400


@pytest.mark.gen_test
def test_adds_client_to_room(hotel_mock_data, http_client, base_url):
    resp = yield http_client.fetch('{}/{}'.format(base_url, 'room-clients'),
                                   method='POST',
                                   raise_error=False,
                                   body=json.dumps({
                                       'client_id': 1,
                                       'room_id': 1
                                   }))

    assert resp.code == 201
    room = session.query(HotelRoom).get(1)
    assert len(room.clients) == 1


@pytest.mark.gen_test
def test_adds_client_to_non_existing_room_raises400(hotel_mock_data,
                                                    http_client, base_url):
    resp = yield http_client.fetch('{}/{}'.format(base_url, 'room-clients'),
                                   method='POST',
                                   raise_error=False,
                                   body=json.dumps({
                                       'client_id': 1,
                                       'room_id': 5
                                   }))

    assert resp.code == 400

@pytest.mark.gen_test
def test_deletes_hotel_room(hotel_mock_data,http_client, base_url):
    resp = yield http_client.fetch(f'{base_url}/rooms/1',
                                   method='DELETE',
                                   raise_error=False)

    assert resp.code == 204

@pytest.mark.gen_test
def test_raises_404_when_deleting_non_existing_room(hotel_mock_data,
                                                    http_client, base_url):
    resp = yield http_client.fetch(f'{base_url}/rooms/5',
                                   method='DELETE',
                                   raise_error=False)

    assert resp.code == 404