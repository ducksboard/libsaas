"""
Premade parser functions for libsaas. Each one takes the response body, HTTP
response code and a dict of headers and should either return a result Python
object or raise HTTPError.
"""
import json

from libsaas import http

# expose the function from the xml module as a parser
from libsaas.xml import parse_xml


def parse_json(body, code, headers):
    if not 200 <= code < 300:
        raise http.HTTPError(body, code, headers)

    # JSON mandates the use of UTF-8, so assume the body is decodable
    return json.loads(body.decode('utf-8'))


def parse_empty(body, code, headers):
    if not 200 <= code < 300:
        raise http.HTTPError(body, code, headers)
