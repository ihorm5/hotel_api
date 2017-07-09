from restless.exceptions import BadRequest
from restless.tnd import TornadoResource
from tornado import gen

from hotel_api.apps.hotels.models import Hotel, HotelRoom, Client
from hotel_api.apps.hotels.preparers import hotel_preparer, room_preparer
from hotel_api.contrib.db.utils import get_or_404

from hotel_api.contrib.db import session


class ValidateMixin(TornadoResource):
    required_fields = ()

    def create(self, *args, **kwargs):
        for f in self.required_fields:
            if f not in self.data:
                raise BadRequest(f'Should provide {f} value')

    def is_authenticated(self):
        return True


class HotelHandler(ValidateMixin):
    model = Hotel
    preparer = hotel_preparer
    required_fields = ('title',)

    @gen.coroutine
    def list(self):
        return session.query(self.model)

    @gen.coroutine
    def detail(self, id):
        return get_or_404(self.model, id)

    def create(self, *args, **kwargs):
        super(HotelHandler, self).create(*args, **kwargs)
        title = self.data.get('title')
        hotel = Hotel(title=title)
        hotel.save()
        return hotel

    def delete(self, id):
        hotel = get_or_404(self.model, id)
        hotel.delete()


class RoomHandler(ValidateMixin):
    model = HotelRoom
    preparer = room_preparer
    required_fields = ('number', 'hotel_id')

    def list(self):
        return session.query(self.model)

    def create(self, *args, **kwargs):
        number = self.data.get('number')
        hotel_id = self.data.get('hotel_id')
        room = HotelRoom(number=number, hotel_id=hotel_id)
        room.save()
        return room

    def delete(self, id):
        hotel_room = get_or_404(HotelRoom, id)
        hotel_room.delete()


class ClientHandler(ValidateMixin):
    """
    We provide only create method here for the sake of simplicity
    """
    required_fields = ('first_name', 'last_name')
    model = Client

    def create(self, *args, **kwargs):
        super(ClientHandler, self).create(*args, **kwargs)
        first_name = self.data.get('first_name')
        last_name = self.data.get('last_name')
        client = Client(first_name=first_name,
                        last_name=last_name)
        client.save()
        return client


class RoomClientsHandler(ValidateMixin):
    required_fields = ('client_id', 'room_id')
    model = HotelRoom
    preparer = room_preparer

    def create(self, *args, **kwargs):
        """
        Logic for deleting should be nearly the same, so I won't provide it
        :param args:
        :param kwargs:
        :return:
        """
        super(RoomClientsHandler, self).create(*args, **kwargs)
        client_id = self.data.get('client_id')
        room_id = self.data.get('room_id')

        room = session.query(HotelRoom).get(room_id)
        client = session.query(Client).get(client_id)

        if not (room and client):
            raise BadRequest('One of client and room does not exist')
        client.rooms.append(room)
        session.add(client)
        session.commit()
        return room


class RoomHotelHandler(ValidateMixin):
    required_fields = ('room_id', 'hotel_id')
    model = Hotel
    preparer = hotel_preparer

    def create(self, *args, **kwargs):
        """
        SQLite doesn't have control over existing FK to other tables
        So I have to check if hotel/room already exists in db
        :param args:
        :param kwargs:
        :return:
        """
        super(RoomHotelHandler, self).create(*args, **kwargs)
        room_id = self.data.get('room_id')
        hotel_id = self.data.get('hotel_id')

        room = session.query(HotelRoom).get(room_id)
        hotel = session.query(Hotel).get(hotel_id)

        if not (room and hotel):
            raise BadRequest('One of hotel and room does not exist')
        hotel.rooms.append(room)
        session.add(hotel)
        session.commit()
        return hotel
