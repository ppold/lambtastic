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
from core.models import Landmark, Museum, HistoricSite, UrbanSite


engine = create_engine(settings.SQLALCHEMY_DB_URI)
Session = sessionmaker(bind=engine)
session = Session()
http = PoolManager()


Dataset = namedtuple('Dataset', ['filename', 'url'])


def unicode_csv_reader(utf8_data, **kwargs):
    csv_reader = csv.reader(utf8_data, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, 'utf-8') for key, value in row.iteritems()}


def convfloat(string):
    """
    >>> convfloat(' -76.85446015010548,-12.22286259231198,')
    [-76.85446015010548, -12.22286259231198]
    """
    values = string.split(',')
    return [float(value) for value in values if value]


class reify(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except:  # pragma: no cover
            pass

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


class Poligon(object):
    # http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon
    def __init__(self, points):
        self.points = points

    @property
    def length(self):
        return len(self.points)

    @reify
    def centroid(self):
        x = 1/(6*self.area) * sum((self.points[i][0] + self.points[i+1][0]) *
                                  (self.points[i][0]*self.points[i+1][1] - self.points[i+1][0]*self.points[i][1])
                                  for i in range(self.length - 1))

        y = 1/(6*self.area) * sum((self.points[i][1] + self.points[i+1][1]) *
                                  (self.points[i][0]*self.points[i+1][1] - self.points[i+1][0]*self.points[i][1])
                                  for i in range(self.length - 1))
        return (y, x)

    @reify
    def area(self):
        return 0.5 * sum(self.points[i][0]*self.points[i+1][1] -
                         self.points[i+1][0]*self.points[i][1]
                         for i in range(self.length - 1))


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
    logging.info('Loading ... %s', dataset.url)
    with open(dataset.filename) as csvfile:
        for row in UnicodeDictReader(csvfile):
            name = row['NOMBRE_DEL_MUSEO']
            museo = session.query(Museum).filter_by(name=name).first()
            if museo:
                logging.info('Found museum with name: "%s"... Skipping', name)
                continue
            landmark = Landmark(latitude=row['LATITUD'],
                                longitude=row['LONGITUD'])
            museo = Museum(name=name,
                           cost=row['COSTO'],
                           phone=row['TELEFONO'],
                           webpage=row['PAGINA_WEB'],
                           schedule=row['HORARIO_ATENCION'],
                           landmark=landmark)
            session.add(museo)
        session.commit()


def load_sitios():
    """Load sitios arqueologicos"""
    dataset = Dataset('sitios.csv', 'http://lima.datosabiertos.pe/datastreams/79519-sitios-arqueologicos-de-lima.csv')
    download_data(dataset.url, dataset.filename)
    logging.info('loading ... %s', dataset.filename)
    with open(dataset.filename) as csvfile:
        for row in unicode_csv_reader(csvfile):
            name = row[0]
            hist_site = session.query(HistoricSite).filter_by(name=name).first()
            if hist_site:
                logging.info('Found historic site with name: "%s"... Skiping', name)
                continue
            points = [convfloat(i) for i in row[2].split('0.0') if i.strip()]  # muahahaha
            poligon = Poligon(points)
            centroid = poligon.centroid
            landmark = Landmark(latitude=centroid[0], longitude=centroid[1])
            hist_site = HistoricSite(name=name, landmark=landmark)
            session.add(hist_site)
        session.commit()


def load_urbanos():
    dataset = Dataset('historicos.csv', 'http://lima.datosabiertos.pe/datastreams/79490-ambientes-urbano-monumentales-en-el-centro-historico-de-lima.csv')
    download_data(dataset.url, dataset.filename)
    logging.info('Loading ...  %s', dataset.filename)
    with open(dataset.filename) as csvfile:
        for row in UnicodeDictReader(csvfile):
            name=row['Nombre de la U.I.']
            urban_site = session.query(UrbanSite).filter_by(name=name).first()
            if urban_site:
                logging.info('Found historic site with name: "%s"... Skiping', name)
                continue
            location = u'{0}, Lima, Peru'.format(name)
            geo = get_geolocation_data(location)
            logging.debug('Received geolocation: %s', geo)
            if not geo['results']:
                logging.warn('Geocoding not found for: "%s"', name)
                landmark = Landmark(
                    # name=name,
                    latitude=None,
                    longitude=None,
                )
            else:
                landmark = Landmark(
                    # name=name,
                    latitude=geo['results'][0]['geometry']['location']['lat'],
                    longitude=geo['results'][0]['geometry']['location']['lng'],
                )
            urban_site = UrbanSite(
                name=name,
                landmark=landmark,
                direction=row['Dirección'],
                description=row['Descripción'],
            )
            session.add(urban_site)
        session.commit()


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Panavision sync')
    parser.add_argument('-l', '--loglevel', dest='loglevel', default='info', type=str, help='Logging level')
    parser.add_argument('-a', '--all', dest='all', action='store_true', help='Load all')
    parser.add_argument('-m', '--museos', dest='museos', action='store_true', help='Load only museos')
    parser.add_argument('-s', '--sitios', dest='sitios', action='store_true', help='Load only sitios arqueologicos')
    parser.add_argument('-u', '--urbanos', dest='urbanos', action='store_true', help='Load only sitios urbanos')
    parser.add_argument('-t', '--test', dest='test', action='store_true', help='testing Bro')
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

    if args.test:
        import doctest
        doctest.testmod(verbose=True)
