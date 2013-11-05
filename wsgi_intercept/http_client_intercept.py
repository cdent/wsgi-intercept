"""
intercept HTTP connections that use httplib or http.client
"""

try:
    import http.client as http_lib
except ImportError:
    import httplib as http_lib

from . import WSGI_HTTPConnection

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

InterceptorMixin = WSGI_HTTPConnection


class HTTP_WSGIInterceptor(InterceptorMixin, http_lib.HTTPConnection):
    pass


class HTTPS_WSGIInterceptor(InterceptorMixin, http_lib.HTTPSConnection):
    pass


def install():
    http_lib.HTTPSConnection = HTTPS_WSGIInterceptor
    http_lib.HTTPConnection = HTTP_WSGIInterceptor


def uninstall():
    http_lib.HTTPConnection = OriginalHTTPConnection
    http_lib.HTTPSConnection = OriginalHTTPSConnection
