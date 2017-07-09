from restless.tnd import TornadoResource
from tornado import gen

from restless.preparers import FieldsPreparer

from hotel_api.apps.customers.models import Hotel
from hotel_api.contrib.db.utils import get_or_404
from hotel_api.contrib.handlers import RestHandler

from hotel_api.contrib.db import session


class HotelHandler(TornadoResource):
    model = Hotel
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'name': 'name',
    })

    @gen.coroutine
    def list(self):
        return session.query(Hotel)

    @gen.coroutine
    def detail(self, id):
        return get_or_404(self.model, id)
