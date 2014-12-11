from __future__ import unicode_literals
import requests
import sys

if sys.version_info.major >= 3:  # pragma: no cover
    from urllib.parse import urlencode
else:  # pragam: no cover
    from urllib import urlencode


class StationQuery(object):

    def __init__(self, text):
        _parameter = {'name': text}
        self._url = 'http://start.vag.de/dm/api/haltestellen.json/vgn?' + \
            urlencode(_parameter)

    def query(self):
        stations = []
        r = requests.get(self._url)
        stations_data = r.json()["Haltestellen"]
        for station_data in stations_data:
            stations.append(Station(station_data["VGNKennung"],
                                    station_data["Haltestellenname"],
                                    station_data["VAGKennung"]))
        return stations


class Station(object):

    def __init__(self, station_id, name, vag_name):
        self.station_id = station_id
        self.name = name
        self.vag_name = vag_name

    def __str__(self):
        if sys.version_info.major >= 3:  # pragma: no cover
            return self.__unicode__()
        else:
            return unicode(self).encode('utf-8')  # NOQA

    def __unicode__(self):
        return '{station_id:5} {vag_name:10} {station_name}'.\
            format(station_id=self.station_id,
                   vag_name=self.vag_name,
                   station_name=self.name)
