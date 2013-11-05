"""
intercept HTTP connections that use requests
"""

import requests
from . import WSGI_HTTPConnection, wsgi_fake_socket
from requests.packages.urllib3.connectionpool import (HTTPConnectionPool,
        HTTPSConnectionPool)
from requests.packages.urllib3.connection import (HTTPConnection,
        HTTPSConnection)
import sys

InterceptorMixin = WSGI_HTTPConnection
wsgi_fake_socket.settimeout = lambda self, timeout: None


class HTTP_WSGIInterceptor(InterceptorMixin, HTTPConnection):
    pass


class HTTPS_WSGIInterceptor(InterceptorMixin, HTTPSConnection):
    pass


def install():
    HTTPConnectionPool.ConnectionCls = HTTP_WSGIInterceptor
    HTTPSConnectionPool.ConnectionCls = HTTPS_WSGIInterceptor


def uninstall():
    HTTPConnectionPool.ConnectionCls = HTTPConnection
    HTTPSConnectionPool.ConnectionCls = HTTPSConnection
