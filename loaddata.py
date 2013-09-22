#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import csv
import logging
from os import path
from collections import namedtuple
try:
    from urllib.request import urlretrieve
except ImportError:  # python2
    from urllib import urlretrieve

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings
from core.models import Landmark, Kind


engine = create_engine(settings.SQLALCHEMY_DB_URI)
Session = sessionmaker(bind=engine)
session = Session()


Dataset = namedtuple('Dataset', ['filename', 'url'])


def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, 'utf-8') for key, value in row.iteritems()}


def download_data(url, filename=None):
    if filename is None:
        filename = path.basename(url)
    if not path.exists(filename):
        urlretrieve(url, filename)


def load_museos():
    dataset = Dataset('museos.csv', 'http://lima.datosabiertos.pe/datastreams/79487-museos-de-lima.csv')
    logging.info('Downloading ...', dataset.url)
    download_data(dataset.url, dataset.filename)
    logging.info('loading ...', dataset.url)
    museo = Kind(name='museo')
    with open(dataset.filename) as csvfile:
        for row in UnicodeDictReader(csvfile):
            landmark = Landmark(
                name=row['NOMBRE_DEL_MUSEO'],
                latitude=row['LATITUD'],
                longitude=row['LONGITUD'],
                kind=museo,
            )
            session.add(landmark)
        session.commit()


def load_arqueologicos():
    """Load sitios arqueologicos"""
    dataset = Dataset('sitios.csv', 'http://lima.datosabiertos.pe/datastreams/79519-sitios-arqueologicos-de-lima.csv')
    logging.info('Downloading ...', dataset.url)
    download_data(dataset.url, dataset.filename)
    logging.info('loading ...', dataset.filename)
    with open(dataset.filename) as csvfile:
        for row in UnicodeDictReader(csvfile):
            landmark = Landmark(
                name=row['NOMBRE_DEL_MUSEO'],
                latitude=row['LATITUD'],
                longitude=row['LONGITUD'],
            )
            session.add(landmark)
        session.commit()


def load_historicos():
    dataset = Dataset('historicos.csv', 'http://lima.datosabiertos.pe/datastreams/79490-ambientes-urbano-monumentales-en-el-centro-historico-de-lima.csv'),
    logging.info('Downloading ...', dataset.url)
    download_data(dataset.url, dataset.filename)
    logging.info('loading ...', dataset.filename)
    with open(dataset.filename) as csvfile:
        for row in UnicodeDictReader(csvfile):
            landmark = Landmark(
                name=row['NOMBRE_DEL_MUSEO'],
                latitude=row['LATITUD'],
                longitude=row['LONGITUD'],
            )
            session.add(landmark)
        session.commit()


if __name__ == '__main__':
    load_museos()
    #load_arqueologicos()
    #load_historicos()
