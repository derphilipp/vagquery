from __future__ import unicode_literals
import datetime
import requests
import sys
import pytz


class Departure(object):

    def __init__(self, direction, direction_type, stopping_point, type_number,
                 departure_actual, departure_planned, product, trip_id,
                 longitude, latitude, prognosis):
        self.direction = direction
        self.direction_type = direction_type
        self.stopping_point = stopping_point
        self.type_number = type_number
        self.departure_actual = departure_actual
        self.departure_planned = departure_planned
        self.product = product
        self.trip_id = trip_id
        self.longitude = longitude
        self.latitude = latitude
        self.prognosis = prognosis

    @property
    def departure_in_min(self):
        departure = self.departure_actual - datetime.datetime.now()
        return int(departure.total_seconds() / 60)

    @property
    def departure_in_min_planned(self):
        departure = self.departure_planned - datetime.datetime.now()
        return int(departure.total_seconds() / 60)

    def __str__(self):
        if sys.version_info.major >= 3:
            return self.__unicode__()  # pragma: no cover
        else:
            return unicode(self).encode('utf-8')  # NOQA

    def __unicode__(self):
        return '{departure:3} {product:5} -> {direction:20} (ID:{trip_id:5})'.\
            format(departure=self.departure_in_min, product=self.product,
                   direction=self.direction, trip_id=self.trip_id)


class DepartureQuery(object):

    def __init__(self, station_id, timedelay=0,
                 bus=True, subway=True, tram=True):
        products_string = self._build_products_string(bus, subway, tram)
        self._url = "http://start.vag.de/dm/api/abfahrten.json/vgn/" +\
            str(station_id) + "/?timedelay=" +\
            str(timedelay) + "&product=" + products_string
        tz = pytz.timezone('Europe/Berlin').localize(
            datetime.datetime.now()).strftime('%z')
        self.tz = tz[:3] + ':' + tz[3:]

    def query(self):
        departures = []
        r = requests.get(self._url)
        data_departures = r.json()["Abfahrten"]

        for departure in data_departures:
            direction = departure["Richtungstext"]
            direction_type = departure["Richtung"]
            stopping_point = departure["Haltepunkt"]
            type_number = departure["Fahrtartnummer"]
            _departure_actual = departure["AbfahrtszeitIst"]
            departure_actual = datetime.datetime.strptime(
                _departure_actual, "%Y-%m-%dT%H:%M:%S" + self.tz)
            _departure_planned = departure["AbfahrtszeitSoll"]
            departure_planned = datetime.datetime.strptime(
                _departure_planned, "%Y-%m-%dT%H:%M:%S" + self.tz)
            product = departure["Produkt"]
            trip_id = departure["Fahrtnummer"]
            longitude = departure["Longitude"]
            latitude = departure["Latitude"]
            prognosis = departure["Prognose"]

            departures.append(
                Departure(
                    direction, direction_type, stopping_point,
                    type_number, departure_actual, departure_planned,
                    product, trip_id, longitude, latitude, prognosis
                ))
        return departures

    @staticmethod
    def _build_products_string(bus, subway, tram):
        text = list()
        if not bus and not subway and not tram:
            raise Exception("No transportation set")
        if subway:
            text.append("Ubahn")
        if bus:
            text.append("Bus")
        if tram:
            text.append("Tram")
        return ','.join(text)
