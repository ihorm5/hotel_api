from tornado.web import URLSpec as url

from .api import HotelHandler


urls = [
    url(r'', HotelHandler.as_list()),
    url(r'\/(?P<id>[\d]+)', HotelHandler.as_detail()),
]
