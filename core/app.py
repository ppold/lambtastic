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
# from .models import *
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
AVATARS_PATH = abspath(join(directory, 'avatars'))

template = functools.partial(template, template_lookup=[TEMPLATE_PATH])


@get("/test")
def test(session):
    """ the whole test """

    response.content_type = "application/json"
    return json.dumps({})
    # return template('index.html')

