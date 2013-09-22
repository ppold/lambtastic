#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" views definitions """

import functools
from os.path import join, dirname, abspath
import simplejson as json
from bottle import jinja2_template as template
from bottle import app, request, response, get, post, redirect, static_file, route
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import desc
import bottle_sqlalchemy
from .models import Landmark, Kind
import settings

# app setup
engine = create_engine(
    settings.SQLALCHEMY_DB_URI,
    echo=settings.SQLALCHEMY_DEBUG is True
)
plugin = bottle_sqlalchemy.Plugin(engine, keyword="session", use_kwargs=True)
app().install(plugin)


directory = dirname(__file__)
TEMPLATE_PATH = abspath(join(directory, 'templates'))
STATIC_PATH = abspath(join(directory, 'static'))

template = functools.partial(template, template_lookup=[TEMPLATE_PATH])


@get('/')
def index():
    """ landing page """
    return template('index.html')


@get('/static/<filepath:path>')
def send_static(filepath):
    """ serves the front-end resources """
    return static_file(filepath, root=STATIC_PATH)


@get("/landmarks/<key:int>")
def landmark(session, key):
    """ returns information about a landmark in particular """

    response.content_type = "application/json"
    data = session.query(Landmark).get(key)
    return json.dumps(data)


@get("/landmarks/museums")
def museums(session):
    """ returns a list of museums """

    response.content_type = "application/json"
    museums_kind = session.query(Kind).filter_by(name="museo").first()
    data = session.query(Landmark).filter_by(kind=museums_kind).all()
    return json.dumps(data)

@get("/landmarks/historic")
def museums(session):
    """ returns a list of museums """

    response.content_type = "application/json"
    historic_kind = session.query(Kind).filter_by(name="Centro Historico").first()
    data = session.query(Landmark).filter_by(kind=historic_kind).all()
    return json.dumps(data)

@get("/landmarks/bikeways")
def bikeways(session):
    """ returns a list of bikeways """

    kind = session.query(Kind).filter_by(name="bikeways").first()
    data = session.query(Landmark).filter_by(kind=kind).all()
    return data
