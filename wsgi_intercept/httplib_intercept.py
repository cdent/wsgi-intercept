
"""intercept HTTP connections that use httplib

(see wsgi_intercept/__init__.py for examples)

"""

import http.client
import wsgi_intercept
import sys
from http.client import (
    HTTPConnection as OriginalHTTPConnection, 
    HTTPSConnection as OriginalHTTPSConnection)

def install():
    http.client.HTTPConnection = wsgi_intercept.WSGI_HTTPConnection
    http.client.HTTPSConnection = wsgi_intercept.WSGI_HTTPSConnection

def uninstall():
    http.client.HTTPConnection = OriginalHTTPConnection
    http.client.HTTPSConnection = OriginalHTTPSConnection
