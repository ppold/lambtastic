#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" views definitions """

from bottle import app, request, response, get, post, redirect
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


@get("/test")
def test(session):
    """ the whole test """

    response.content_type = "application/json"
    return json.dumps({})

