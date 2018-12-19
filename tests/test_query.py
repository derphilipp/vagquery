#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import pytest
import vagquery

import responses


@pytest.fixture(scope="session")
def my_responses():
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
    }"""
    status = 200
    content_type = "application/json"
    responses.add(
        responses.GET, url_re, body=body, status=status, content_type=content_type
    )
    yield responses


@pytest.fixture(scope="session")
@responses.activate
def query_result(my_responses):
    station = vagquery.StationQuery("Schweigger")
    result = station.query()
    return result


@pytest.fixture(scope="session")
def station(query_result):
    station = query_result[0]
    return station


def test_assert_single_query_result(query_result):
    assert query_result[0].vag_name == "SCHW"
    assert len(query_result) == 1


def test_station_name(station):
    assert station.name == u"Schweiggerstr. (Nürnberg)"


def test_station_id(station):
    assert station.station_id == 536


def test_station_vag_name(station):
    assert station.vag_name == "SCHW"


def test_station_string(station):
    assert str(station) == "  536 SCHW       Schweiggerstr. (Nürnberg)"


def test_station_unicode(station):
    assert station.__unicode__() == u"  536 SCHW       Schweiggerstr. (Nürnberg)"
