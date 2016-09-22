"""Test response header validations.

Response headers are supposed to be bytestrings and some servers,
notably will experience an error if they are given headers with
the wrong form. Since wsgi-intercept is standing in as a server,
it should behave like one on this front. At the moment it does
not. There are tests for how it delivers request headers, but
not the other way round. Let's write some tests to fix that.
"""

import py.test
import requests

import wsgi_intercept
from wsgi_intercept.interceptor import RequestsInterceptor


class HeaderApp(object):
    """A simple app that returns whatever headers we give it."""

    def __init__(self, headers):
        self.headers = headers

    def __call__(self, environ, start_response):

        headers = []
        for header in self.headers:
            headers.append((header, self.headers[header]))
        start_response('200 OK', headers)
        return ['']


def app(headers):
    return HeaderApp(headers)


def test_header_app():
    """Make sure the header apps returns headers.

    Many libraries normalize headers to strings so we're not
    going to get exact matches.
    """
    header_value = b'alpha'
    header_value_str = 'alpha'

    def header_app():
        return app({'request-id': header_value})

    with RequestsInterceptor(header_app) as url:
        response = requests.get(url)

    assert response.headers['request-id'] == header_value_str


def test_encoding_violation():
    """If the header is unicode we expect boom."""
    header_value = u'alpha'

    def header_app():
        return app({'request-id': header_value})

    # save original
    strict_response_headers = wsgi_intercept.STRICT_RESPONSE_HEADERS

    # With STRICT_RESPONSE_HEADERS True, response headers must be
    # bytestrings.
    with RequestsInterceptor(header_app) as url:
        wsgi_intercept.STRICT_RESPONSE_HEADERS = True

        with py.test.raises(TypeError) as error:
            response = requests.get(url)

        assert (str(error.value) ==
            'Header request-id has value alpha which is not a bytestring.')

        # When False, other types of strings are okay.
        wsgi_intercept.STRICT_RESPONSE_HEADERS = False

        response = requests.get(url)

        assert response.headers['request-id'] == header_value

    # reset back to saved original
    wsgi_intercept.STRICT_RESPONSE_HEADERS = \
        strict_response_headers
