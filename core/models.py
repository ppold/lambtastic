# -*- coding: utf-8 -*-

import uuid

from sqlalchemy import Column, Integer, Unicode, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Landmark(Base):
    __tablename__ = 'landmark'

    id = Column(Integer, primary_key=True)
    guid = Column(String, nullable=False)
    latitude = Column(String)
    longitude = Column(String)

    def __init__(self, **kwargs):
        guid = uuid.uuid4()
        kwargs.setdefault('guid', guid)
        super(Landmark, self).__init__(**kwargs)

    def _asdict(self):
        return {
            'id': self.key,
            'guid': self.guid,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }


class Museum(Base):
    __tablename__ = 'museum'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cost = Column(Unicode)
    webpage = Column(String)
    schedule = Column(Unicode)
    description = Column(Unicode)

    landmark_id = Column(Integer, ForeignKey('landmark.id'))
    landmark = relationship('Landmark', backref=backref('museo', uselist=False))

    def _asdict(self):
        return {
            'id': self.id,
            'kind': 'museo',
            'name': self.name,
            'cost': self.costo,
            'webpage': self.webpageo,
            'schedule': self.scheduleo,
            'latitude': self.location.latitude,
            'longitude': self.location.longitude,
            'description': self.description,
        }


class HistoricSite(Base):
    __tablename__ = 'historic_site'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)

    landmark_id = Column(Integer, ForeignKey('landmark.id'))
    landmark = relationship('Landmark', backref=backref('historic_site', uselist=False))

    def _asdict(self):
        return {
            'id': self.id,
            'kind': 'historic',
            'name': self.name,
            'latitude': self.location.latitude,
            'longitude': self.location.longitude,
        }


class UrbanSite(Base):
    __tablename__ = 'urban_site'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    direction = Column(Unicode)
    description = Column(Unicode)

    landmark_id = Column(Integer, ForeignKey('landmark.id'))
    landmark = relationship('Landmark', backref=backref('urban_site', uselist=False))

    def _asdict(self):
        return {
            'id': self.id,
            'kind': 'urban',
            'name': self.name,
            'direction': self.direction,
            'latitude': self.location.latitude,
            'longitude': self.location.longitude,
        }
