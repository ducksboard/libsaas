"""
Premade parser functions for libsaas. Each one takes the response body, HTTP
response code and a dict of headers and should either return a result Python
object or raise HTTPError.
"""
import json

from libsaas import http


def parse_json(body, code, headers):
    if not 200 <= code < 300:
        raise http.HTTPError(body, code, headers)
    return json.loads(body)


def parse_empty(body, code, headers):
    if not 200 <= code < 300:
        raise http.HTTPError(body, code, headers)
