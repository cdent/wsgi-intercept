"""
Simple WSGI applications for testing.
"""

from pprint import pformat

try:
    bytes
except ImportError:
    bytes = str


class MockWSGIApp(object):
    def __init__(self, app):
        self._app = app
        self._hits = 0
        self._internals = {}

    def __call__(self, environ, start_response):
        self._hits += 1
        self._internals = environ
        return self._app(environ, start_response)

    def reset(self):
        self._hits = 0
        self._internals = {}

    def success(self):
        return self._hits > 0

    def get_internals(self):
        return self._internals


def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [b'WSGI intercept successful!\n']


def more_interesting_app(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return [pformat(environ).encode('utf-8')]


def raises_app(environ, start_response):
    raise TypeError("bah")
