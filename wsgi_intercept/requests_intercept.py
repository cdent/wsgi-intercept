"""Intercept HTTP connections that use `requests <http://docs.python-requests.org/en/latest/>`_.
"""

import sys

from . import WSGI_HTTPConnection, WSGI_HTTPSConnection, wsgi_fake_socket
from requests.packages.urllib3.connectionpool import (HTTPConnectionPool,
        HTTPSConnectionPool)
from requests.packages.urllib3.connection import (HTTPConnection,
        HTTPSConnection)


wsgi_fake_socket.settimeout = lambda self, timeout: None


class HTTP_WSGIInterceptor(WSGI_HTTPConnection, HTTPConnection):
    def __init__(self, *args, **kwargs):
        if 'strict' in kwargs and sys.version_info > (3, 0):
            kwargs.pop('strict')
        WSGI_HTTPConnection.__init__(self, *args, **kwargs)
        HTTPConnection.__init__(self, *args, **kwargs)


class HTTPS_WSGIInterceptor(WSGI_HTTPSConnection, HTTPSConnection):
    is_verified = True

    def __init__(self, *args, **kwargs):
        if 'strict' in kwargs and sys.version_info > (3, 0):
            kwargs.pop('strict')
        WSGI_HTTPSConnection.__init__(self, *args, **kwargs)
        HTTPSConnection.__init__(self, *args, **kwargs)


def install():
    HTTPConnectionPool.ConnectionCls = HTTP_WSGIInterceptor
    HTTPSConnectionPool.ConnectionCls = HTTPS_WSGIInterceptor


def uninstall():
    HTTPConnectionPool.ConnectionCls = HTTPConnection
    HTTPSConnectionPool.ConnectionCls = HTTPSConnection
