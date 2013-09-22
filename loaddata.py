#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import csv
import json
import logging
from os import path
from collections import namedtuple
try:
    from urllib.request import urlretrieve
except ImportError:  # python2
    from urllib import urlretrieve

from urllib3 import PoolManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings
from core.models import Landmark, Kind


engine = create_engine(settings.SQLALCHEMY_DB_URI)
Session = sessionmaker(bind=engine)
session = Session()
http = PoolManager()


Dataset = namedtuple('Dataset', ['filename', 'url'])


def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, 'utf-8') for key, value in row.iteritems()}


def get_geolocation_data(address):
    """Get gps information about a given address."""
    url = 'http://maps.googleapis.com/maps/api/geocode/json'
    fields = {'address': address.encode('utf-8'), 'sensor': 'false', 'region': 'pe'}
    resp = http.request('GET', url, fields=fields)
    return json.loads(resp.data)


def download_data(url, filename=None):
    logging.info('Downloading ... %s', url)
    if filename is None:
        filename = path.basename(url)
    if not path.exists(filename):
        urlretrieve(url, filename)


def load_museos():
    dataset = Dataset('museos.csv', 'http://lima.datosabiertos.pe/datastreams/79487-museos-de-lima.csv')
    download_data(dataset.url, dataset.filename)
    museo = Kind(name=u'museo')
    logging.info('Loading ... %s', dataset.url)
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


def load_sitios():
    """Load sitios arqueologicos"""
    dataset = Dataset('sitios.csv', 'http://lima.datosabiertos.pe/datastreams/79519-sitios-arqueologicos-de-lima.csv')
    download_data(dataset.url, dataset.filename)
    logging.info('loading ... %s', dataset.filename)
    return
    with open(dataset.filename) as csvfile:
        for row in UnicodeDictReader(csvfile):
            landmark = Landmark(
                name=row['NOMBRE_DEL_MUSEO'],
                latitude=row['LATITUD'],
                longitude=row['LONGITUD'],
            )
            session.add(landmark)
        session.commit()


def load_urbanos():
    dataset = Dataset('historicos.csv', 'http://lima.datosabiertos.pe/datastreams/79490-ambientes-urbano-monumentales-en-el-centro-historico-de-lima.csv')
    download_data(dataset.url, dataset.filename)
    historico = Kind(name=u'Centro Historico')
    logging.info('Loading ...  %s', dataset.filename)
    with open(dataset.filename) as csvfile:
        for row in UnicodeDictReader(csvfile):
            location = u'{0} {1}, Lima, Peru'.format(row['Dirección'], row[''])  # LOL
            geo = get_geolocation_data(location)
            logging.debug('Received geolocation: %s', geo)
            if not geo['results']:
                landmark = Landmark(
                    kind=historico,
                    name=row['Ubicación'],
                    latitude=None,
                    longitude=None,
                )
            else:
                landmark = Landmark(
                    kind=historico,
                    name=row['Ubicación'],
                    latitude=geo['results'][0]['geometry']['location']['lat'],
                    longitude=geo['results'][0]['geometry']['location']['lng'],
                )
            session.add(landmark)
        session.commit()


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Panavision sync')
    parser.add_argument('-l', '--loglevel', dest='loglevel', default='info', type=str, help='Logging level')
    parser.add_argument('-a', '--all', dest='all', action='store_true', help='Load all')
    parser.add_argument('-m', '--museos', dest='museos', action='store_true', help='Load only museos')
    parser.add_argument('-s', '--sitios', dest='sitios', action='store_true', help='Load only sitios arqueologicos')
    parser.add_argument('-u', '--urbanos', dest='urbanos', action='store_true', help='Load only sitios urbanos')
    args = parser.parse_args()
    level = getattr(logging, args.loglevel.upper(), logging.INFO)
    logging.basicConfig(level=level)

    # Clean me maybe
    if args.all:
        load_museos()
        load_sitios()
        load_urbanos()

    if args.museos:
        load_museos()

    if args.sitios:
        load_sitios()

    if args.urbanos:
        load_urbanos()
