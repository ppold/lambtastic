""" model definitions """

from sqlalchemy import Column, Integer, Date, Unicode, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

class PKMixin:
    """ primary key mixin for the rest of the models """
    key = Column(Integer, primary_key=True)


class EnumMixin:
    """ base model for enumerated values """

    name = Column(Unicode, nullable=False)
    order = Column(Integer, autoincrement=True)


class Kind(BASE, PKMixin, EnumMixin):
    """ Kind of landmark, like a museum, historic site, etc """

    __tablename__ = "kind"


class Landmark(BASE, PKMixin, EnumMixin):
    """ a point of interest """

    __tablename__ = "landmark"
    kind_id = Column(Integer, ForeignKey('kind.key'))

    latitude = Column(String)
    longitude = Column(String)
    kind = relationship(Kind, uselist=False)
