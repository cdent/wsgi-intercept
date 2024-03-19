"""Common code of urllib3 (<2.0.0) and requests intercepts."""

import os
import sys

from . import WSGI_HTTPConnection, WSGI_HTTPSConnection, wsgi_fake_socket


wsgi_fake_socket.settimeout = lambda self, timeout: None

HTTP_KEYWORD_POPS = [
    'strict',
    'socket_options',
    'server_hostname',
]

HTTPS_KEYWORD_POPS = HTTP_KEYWORD_POPS + [
    'key_password',
    'server_hostname',
    'cert_reqs',
    'ca_certs',
    'ca_cert_dir',
    'assert_hostname',
    'assert_fingerprint',
    'ssl_version',
    'ssl_minimum_version',
    'ssl_maximum_version',
]

def make_urllib3_override(HTTPConnectionPool, HTTPSConnectionPool,
                          HTTPConnection, HTTPSConnection):

    class HTTP_WSGIInterceptor(WSGI_HTTPConnection, HTTPConnection):
        def __init__(self, *args, **kwargs):
            print(f"http pre: {args} ::: {kwargs}")
            for kw in HTTP_KEYWORD_POPS:
                kwargs.pop(kw, None)
            WSGI_HTTPConnection.__init__(self, *args, **kwargs)
            HTTPConnection.__init__(self, *args, **kwargs)

    class HTTPS_WSGIInterceptor(WSGI_HTTPSConnection, HTTPSConnection):
        is_verified = True

        def __init__(self, *args, **kwargs):
            print(f"https pre: {args} ::: {kwargs}")
            for kw in HTTPS_KEYWORD_POPS:
                kwargs.pop(kw, None)
            if sys.version_info > (3, 12):
                kwargs.pop('key_file', None)
                kwargs.pop('cert_file', None)
            print(f"https post: {args} ::: {kwargs}")
            host = kwargs.pop('host')
            port = kwargs.pop('port')
            WSGI_HTTPSConnection.__init__(self, host, port, *args, **kwargs)
            print("after wsgi")
            HTTPSConnection.__init__(self, *args, **kwargs)
            print("after https")

    def install():
        if 'http_proxy' in os.environ or 'https_proxy' in os.environ:
            raise RuntimeError(
                'http_proxy or https_proxy set in environment, please unset')
        HTTPConnectionPool.ConnectionCls = HTTP_WSGIInterceptor
        HTTPSConnectionPool.ConnectionCls = HTTPS_WSGIInterceptor

    def uninstall():
        HTTPConnectionPool.ConnectionCls = HTTPConnection
        HTTPSConnectionPool.ConnectionCls = HTTPSConnection

    return install, uninstall
