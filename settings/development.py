""" development configuration """

import os
from .common import *

BOTTLE_DEBUG = True
BOTTLE_AUTORELOAD = True
SQLALCHEMY_DEBUG = True
SQLALCHEMY_DB_URI = os.getenv('SQLALCHEMY_DB_URI',
                              'sqlite:///lambtastic.db')
