from tornado.web import URLSpec as url

from .api import HotelHandler, RoomHandler, RoomHotelHandler, RoomClientsHandler

urls = [
    url(r'hotels', HotelHandler.as_list()),
    url(r'hotels\/(?P<id>[\d]+)', HotelHandler.as_detail()),
    url(r'rooms', RoomHandler.as_list()),
    url(r'rooms\/(?P<id>[\d]+)', RoomHandler.as_detail()),
    url(r'hotel-rooms', RoomHotelHandler.as_list()),
    url(r'room-clients', RoomClientsHandler.as_list())
]
