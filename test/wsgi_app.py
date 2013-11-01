"""
Simple WSGI applications for testing.
"""

from pprint import pformat

try:
    bytes
except ImportError:
    bytes = str


_app_was_hit = False
_internals = {}


def success():
    return _app_was_hit


def get_internals():
    return _internals


def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)

    global _app_was_hit
    _app_was_hit = True

    return [b'WSGI intercept successful!\n']


def create_fn():
    global _app_was_hit
    _app_was_hit = False
    return simple_app


def create_mi():
    global _internals
    _internals = {}
    return more_interesting_app


def more_interesting_app(environ, start_response):
    global _internals
    _internals = environ

    start_response('200 OK', [('Content-type', 'text/plain')])
    return [pformat(environ).encode('utf-8')]
