#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import pytest
import vagquery

import responses
from freezegun import freeze_time


@pytest.fixture(scope="session")
def my_response():
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
    }"""
    status = 200
    content_type = "application/json"
    responses.add(
        responses.GET, url_re, body=body, status=status, content_type=content_type
    )
    yield responses


@pytest.fixture(scope="session")
@responses.activate
def departure(my_response):
    dq = vagquery.DepartureQuery(536, timedelay=0, bus=True, subway=True, tram=True)
    print(dq)
    departures = dq.query()
    return departures[0]


@freeze_time("2014-11-24 18:00:00")
def test_departure_with_delay(departure):
    assert departure.departure_in_min_planned == 4


@freeze_time("2014-11-24 18:00:00")
def test_string(departure):
    assert str(departure) == "  6 Tram  -> Tristanstraße        (ID: 1350)"


@freeze_time("2014-11-24 18:00:00")
def test_unicode(departure):
    assert departure.__unicode__() == u"  6 Tram  -> Tristanstraße        (ID: 1350)"


@freeze_time("2014-11-24 18:00:00")
def test_departure(departure):
    assert departure.departure_in_min == 6
