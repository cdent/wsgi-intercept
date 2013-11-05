
"""intercept HTTP connections that use httplib2

(see wsgi_intercept/__init__.py for examples)

"""

from . import WSGI_HTTPConnection, HTTPConnection, HTTPSConnection
from httplib2 import (SCHEME_TO_CONNECTION, HTTPConnectionWithTimeout,
        HTTPSConnectionWithTimeout)
import sys

InterceptorMixin = WSGI_HTTPConnection


class HTTP_WSGIInterceptorWithTimeout(InterceptorMixin,
        HTTPConnectionWithTimeout):
    def __init__(self, host, port=None, strict=None, timeout=None,
            proxy_info=None, source_address=None):

        # In Python3 strict is deprecated
        if sys.version_info[0] < 3:
            try:
                HTTPConnection.__init__(self, host, port=port, strict=strict,
                        timeout=timeout, source_address=source_address)
            except TypeError:  # Python 2.6 doesn't have source_address
                HTTPConnection.__init__(self, host, port=port, strict=strict,
                        timeout=timeout)
        else:
            HTTPConnection.__init__(self, host, port=port,
                    timeout=timeout, source_address=source_address)


class HTTPS_WSGIInterceptorWithTimeout(InterceptorMixin,
        HTTPSConnectionWithTimeout):
    def __init__(self, host, port=None, strict=None, timeout=None,
            proxy_info=None, ca_certs=None, source_address=None,
            disable_ssl_certificate_validation=False):

        # ignore proxy_info and ca_certs
        # In Python3 strict is deprecated
        if sys.version_info[0] < 3:
            try:
                HTTPSConnection.__init__(self, host, port=port, strict=strict,
                        timeout=timeout, source_address=source_address)
            except TypeError:  # Python 2.6 doesn't have source_address
                HTTPSConnection.__init__(self, host, port=port, strict=strict,
                        timeout=timeout)
        else:
            HTTPSConnection.__init__(self, host, port=port,
                    timeout=timeout, source_address=source_address)


def install():
    SCHEME_TO_CONNECTION['http'] = HTTP_WSGIInterceptorWithTimeout
    SCHEME_TO_CONNECTION['https'] = HTTPS_WSGIInterceptorWithTimeout


def uninstall():
    SCHEME_TO_CONNECTION['http'] = HTTPConnectionWithTimeout
    SCHEME_TO_CONNECTION['https'] = HTTPSConnectionWithTimeout
