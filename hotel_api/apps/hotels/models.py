from hotel_api.contrib.db import Model

from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

association_table = Table('association', Model.metadata,
                          Column('left_id', Integer,
                                 ForeignKey('hotelrooms.id')),
                          Column('right_id', Integer, ForeignKey('clients.id'))
                          )


class Hotel(Model):
    __tablename__ = 'hotels'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(60), nullable=False)
    rooms = relationship("HotelRoom", back_populates="hotel")


class HotelRoom(Model):
    __tablename__ = 'hotelrooms'

    id = Column('id', Integer, primary_key=True)
    number = Column('number', Integer, unique=True)
    hotel_id = Column('hotel', Integer, ForeignKey('hotels.id'))
    hotel = relationship('Hotel')
    clients = relationship('Client',
                           secondary=association_table,
                           )


class Client(Model):
    __tablename__ = 'clients'

    id = Column('id', Integer, primary_key=True)
    first_name = Column('first_name', String(60))
    last_name = Column('last_name', String(60))

    rooms = relationship('HotelRoom',
                         secondary=association_table,
                         )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
