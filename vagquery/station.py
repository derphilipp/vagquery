import requests
import urllib

class StationQuery(object):
    def __init__(self, text):
        parameter = {'name':text}
        self._url = 'http://start.vag.de/dm/api/haltestellen.json/vgn?'+urllib.urlencode(parameter)
    def query(self):
        stations = []
        r = requests.get(self._url)
        stations_data = r.json()["Haltestellen"]
        for station_data in stations_data:
            stations.append(Station(station_data["VGNKennung"],station_data["Haltestellenname"],station_data["VAGKennung"]))
        return stations

class Station(object):
    def __init__(self, station_id, name, vag_name):
        self.station_id = station_id
        self.name = name
        self.vag_name = vag_name

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'{station_id:5} {vag_name:10} {station_name})'.format(station_id = self.station_id, vag_name = self.vag_name, station_name=self.name)

