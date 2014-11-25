# -*- coding: utf-8 -*-
import responses
import unittest
import re
import vagquery
import datetime


class Test_vag_query(unittest.TestCase):
    def add_response(self):
        url_re = re.compile(r'http://start.vag.de/dm/api/haltestellen.json/.*')
        body = """{
        "Haltestellen": [
            {
            "Haltestellenname": "Schweiggerstr. (Nürnberg)",
            "VAGKennung": "SCHW",
            "VGNKennung": 536,
            "Longitude": 11.090035,
            "Latitude": 49.441491,
            "Produkte": "Bus,Tram"
            }
        ]
        }
       """
        status = 200
        content_type = 'application/json'
        responses.add(responses.GET, url_re, body=body, status=status,
                      content_type=content_type)

    @responses.activate
    def setUp(self):
        self.add_response()
        station = vagquery.StationQuery("Schweigger")
        self.result = station.query()
        self.station = self.result[0]

    def test_one_result(self):
        self.assertEqual(1, len(self.result))

    def test_station_id(self):
        self.assertEqual(536, self.station.station_id)

    def test_station_name(self):
        self.assertEqual(u"Schweiggerstr. (Nürnberg)", self.station.name)

    def test_shortname(self):
        self.assertEqual("SCHW", self.station.vag_name)

    def test_string(self):
        self.assertEqual("  536 SCHW       Schweiggerstr. (Nürnberg))",
                         str(self.station))

    def test_unicode(self):
        self.assertEqual(u"  536 SCHW       Schweiggerstr. (Nürnberg))",
                         self.station.__unicode__())


class Test_vag_departure(unittest.TestCase):
    def add_response(self):
        url_re = re.compile(r'http://start.vag.de/dm/api/abfahrten.json/.*')
        body = """{
        "Abfahrten": [
            {
            "Linienname": "8",
            "Haltepunkt": "SCHW:14",
            "Richtung": "Richtung2",
            "Richtungstext": "Tristanstraße",
            "AbfahrtszeitSoll": "2014-11-24T18:04:00+01:00",
            "AbfahrtszeitIst": "2014-11-24T18:06:15+01:00",
            "Produkt": "Tram",
            "Longitude": 11.08954778,
            "Latitude": 49.44187694,
            "Fahrtnummer": 1350,
            "Fahrtartnummer": 1,
            "Prognose": true
            },
            {
            "Linienname": "6",
            "Haltepunkt": "SCHW:11",
            "Richtung": "Richtung1",
            "Richtungstext": "Westfriedhof",
            "AbfahrtszeitSoll": "2014-11-24T18:07:00+01:00",
            "AbfahrtszeitIst": "2014-11-24T18:07:38+01:00",
            "Produkt": "Tram",
            "Longitude": 11.09057278,
            "Latitude": 49.44167,
            "Fahrtnummer": 1499,
            "Fahrtartnummer": 1,
            "Prognose": true
            }
        ]
        }
       """
        status = 200
        content_type = 'application/json'
        responses.add(responses.GET, url_re, body=body, status=status,
                      content_type=content_type)

    @responses.activate
    def setUp(self):
        class FakeDate(datetime.datetime):
            @classmethod
            def now(cls):
                return cls(2014, 11, 24, 18, 00, 00)
        datetime.date = FakeDate
        datetime.datetime = FakeDate
        self.add_response()
        dq = vagquery.DepartureQuery(536, timedelay=0,
                                     bus=True, subway=True, tram=True)
        result = dq.query()
        self.departure = result[0]

    def test_departure(self):
        self.assertEquals(6, self.departure.departure_in_min)

    def test_departure_with_delay(self):
        self.assertEquals(4, self.departure.departure_in_min_planned)

    def test_string(self):
        self.assertEquals(
            "  6 Tram  -> Tristanstraße        (ID: 1350)",
            str(self.departure))

    def test_unicode(self):
        self.assertEquals(
            u"  6 Tram  -> Tristanstraße        (ID: 1350)",
            self.departure.__unicode__())


class Test_vag_departure_with_errors(unittest.TestCase):
    def add_response(self):
        url_re = re.compile(r'http://start.vag.de/dm/api/abfahrten.json/.*')
        body = """{
        "Abfahrten": [
        ]
        }
       """
        status = 200
        content_type = 'application/json'
        responses.add(responses.GET, url_re, body=body, status=status,
                      content_type=content_type)

    @responses.activate
    def test_station_without_any_transportation(self):
        self.add_response()
        self.assertRaises(
            Exception,
            vagquery.DepartureQuery, 536, timedelay=0,
            bus=False, subway=False, tram=False
        )
