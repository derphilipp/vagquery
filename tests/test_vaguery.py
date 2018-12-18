# -*- coding: utf-8 -*-
import pytest
import responses
import re
import datetime
import vagquery


class Test_vag_query:
    def add_response(self):
        url_re = re.compile(r"http://start.vag.de/dm/api/haltestellen.json/.*")
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
        content_type = "application/json"
        responses.add(
            responses.GET, url_re, body=body, status=status, content_type=content_type
        )

    @responses.activate
    @pytest.fixture(autouse=True)
    def setup(self):
        self.add_response()
        station = vagquery.StationQuery("Schweigger")
        self.result = station.query()
        self.station = self.result[0]

    def test_one_result(self):
        assert len(self.result) == 1

    def test_station_id(self):
        assert self.station.station_id == 536

    def test_station_name(self):
        assert self.station.name == u"Schweiggerstr. (Nürnberg)"

    def test_shortname(self):
        assert self.station.vag_name == "SCHW"

    def test_string(self):
        assert str(self.station) == "  536 SCHW       Schweiggerstr. (Nürnberg)"

    def test_unicode(self):
        assert (
            self.station.__unicode__() == u"  536 SCHW       Schweiggerstr. (Nürnberg)"
        )


class Test_vag_departure:
    def add_response(self):
        url_re = re.compile(r"http://start.vag.de/dm/api/abfahrten.json/.*")
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
        content_type = "application/json"
        responses.add(
            responses.GET, url_re, body=body, status=status, content_type=content_type
        )

    @responses.activate
    @pytest.fixture(autouse=True)
    def setup(self):
        class FakeDate(datetime.datetime):
            @classmethod
            def now(cls):
                return cls(2014, 11, 24, 18, 00, 00)

        datetime.date = FakeDate
        datetime.datetime = FakeDate
        self.add_response()
        dq = vagquery.DepartureQuery(536, timedelay=0, bus=True, subway=True, tram=True)
        result = dq.query()
        self.departure = result[0]

    def test_departure(self):
        assert self.departure.departure_in_min == 6

    def test_departure_with_delay(self):
        assert self.departure.departure_in_min_planned == 4

    def test_string(self):
        assert str(self.departure) == "  6 Tram  -> Tristanstraße        (ID: 1350)"

    def test_unicode(self):
        assert (
            self.departure.__unicode__()
            == u"  6 Tram  -> Tristanstraße        (ID: 1350)"
        )


class Test_vag_departure_with_errors:
    @pytest.fixture(autouse=True)
    def add_response(self):
        url_re = re.compile(r"http://start.vag.de/dm/api/abfahrten.json/.*")
        body = """{
        "Abfahrten": [
        ]
        }
       """
        status = 200
        content_type = "application/json"
        responses.add(
            responses.GET, url_re, body=body, status=status, content_type=content_type
        )

    @responses.activate
    def test_station_without_any_transportation(self):
        self.add_response()
        pytest.raises(
            Exception,
            vagquery.DepartureQuery,
            536,
            timedelay=0,
            bus=False,
            subway=False,
            tram=False,
        )
