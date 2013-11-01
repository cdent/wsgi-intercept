
"""intercept HTTP connections that use httplib

(see wsgi_intercept/__init__.py for examples)

"""

# XXX: HTTPSConnection is currently not allowed as attempting
# to override it causes a recursion error.

SKIP_SSL = False

try:
    import http.client as http_lib
    SKIP_SSL = True
except ImportError:
    import httplib as http_lib

from . import WSGI_HTTPConnection, WSGI_HTTPSConnection

try:
    from http.client import (
            HTTPConnection as OriginalHTTPConnection,
            HTTPSConnection as OriginalHTTPSConnection
    )
except ImportError:
    from httplib import (
            HTTPConnection as OriginalHTTPConnection,
            HTTPSConnection as OriginalHTTPSConnection
    )


class Error_HTTPSConnection(object):

    def __init__(self, *args, **kwargs):
        raise NotImplementedError('HTTPS temporarily not implemented')


def install():
    http_lib.HTTPConnection = WSGI_HTTPConnection
    if SKIP_SSL:
        http_lib.HTTPSConnection = Error_HTTPSConnection
    else:
        http_lib.HTTPSConnection = WSGI_HTTPSConnection


def uninstall():
    http_lib.HTTPConnection = OriginalHTTPConnection
    http_lib.HTTPSConnection = OriginalHTTPSConnection
