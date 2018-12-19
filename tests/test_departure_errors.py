# import datetime
# import re

# import pytest
# import vagquery

# import responses
# from freezegun import freeze_time


# class Test_vag_departure_with_errors:
#     @pytest.fixture(autouse=True)
#     def add_response(self):
#         url_re = re.compile(r"http://start.vag.de/dm/api/abfahrten.json/.*")
#         body = """{
#         "Abfahrten": [
#         ]
#         }"""
#         status = 200
#         content_type = "application/json"
#         responses.add(
#             responses.GET, url_re, body=body, status=status, content_type=content_type
#         )

#     @responses.activate
#     def test_station_without_any_transportation(self):
#         pytest.raises(
#             Exception,
#             vagquery.DepartureQuery,
#             536,
#             timedelay=0,
#             bus=False,
#             subway=False,
#             tram=False,
#         )
