from tornado import web
from tornado.web import URLSpec as url

from hotel_api.contrib.urls import include

from hotel_api.settings import settings

urls = [
    url(r"/docs/version/(.*)", web.StaticFileHandler,
        {"path": settings.DOCS_ROOT}),
    url(r"/static/(.*)", web.StaticFileHandler,
        {"path": settings.STATIC_ROOT})
]

urls += include(r'/', "apps.hotels.urls")
