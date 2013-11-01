"""
intercept HTTP connections that use requests
"""

import requests
import wsgi_intercept
from requests.packages.urllib3.connectionpool import (HTTPConnectionPool,
        HTTPSConnectionPool)
from requests.packages.urllib3.connection import (HTTPConnection,
        HTTPSConnection)
import sys

InterceptorMixin = wsgi_intercept.WSGI_HTTPConnection

wsgi_intercept.wsgi_fake_socket.settimeout = lambda self, timeout: None


def our_connect(self):
    """
    Override the connect() function to intercept calls to certain
    host/ports.
    """
    if wsgi_intercept.debuglevel:
        sys.stderr.write('connect: %s, %s\n' % (self.host, self.port,))

    (app, script_name) = self.get_app(self.host, self.port)
    if app:
        if wsgi_intercept.debuglevel:
            sys.stderr.write('INTERCEPTING call to %s:%s\n' %
                             (self.host, self.port,))
        self.sock = wsgi_intercept.wsgi_fake_socket(app,
                                                    self.host, self.port,
                                                    script_name)
    else:
        self._connect()


class HTTP_WSGIInterceptor(InterceptorMixin, HTTPConnection):
    _connect = requests.packages.urllib3.connection.HTTPConnection.connect
    connect = our_connect


class HTTPS_WSGIInterceptor(InterceptorMixin, HTTPSConnection):
    _connect = requests.packages.urllib3.connection.HTTPSConnection.connect
    connect = our_connect


def install():
    HTTPConnectionPool.ConnectionCls = HTTP_WSGIInterceptor
    HTTPSConnectionPool.ConnectionCls = HTTPS_WSGIInterceptor


def uninstall():
    HTTPConnectionPool.ConnectionCls = HTTPConnection
    HTTPSConnectionPool.ConnectionCls = HTTPSConnection
