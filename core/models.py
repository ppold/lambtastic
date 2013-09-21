""" model definitions """

from sqlalchemy import Column, Integer, Text, Date, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class Example(BASE):
    """ model example """

    __tablename__ = "example"

    key = Column(Integer, primary_key=True)
