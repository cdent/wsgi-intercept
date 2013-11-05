"""
intercept HTTP connections that use httplib or http.client
"""

try:
    import http.client as http_lib
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

HTTPInterceptorMixin = WSGI_HTTPConnection
HTTPSInterceptorMixin = WSGI_HTTPSConnection


class HTTP_WSGIInterceptor(HTTPInterceptorMixin, http_lib.HTTPConnection):
    pass


class HTTPS_WSGIInterceptor(HTTPSInterceptorMixin, http_lib.HTTPSConnection,
        HTTP_WSGIInterceptor):
    pass


def install():
    http_lib.HTTPConnection = HTTP_WSGIInterceptor
    http_lib.HTTPSConnection = HTTPS_WSGIInterceptor


def uninstall():
    http_lib.HTTPConnection = OriginalHTTPConnection
    http_lib.HTTPSConnection = OriginalHTTPSConnection
