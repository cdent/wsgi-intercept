
"""intercept HTTP connections that use httplib

(see wsgi_intercept/__init__.py for examples)

"""

import httplib
import wsgi_intercept
import sys
from httplib import (
    HTTPConnection as OriginalHTTPConnection, 
    HTTPSConnection as OriginalHTTPSConnection)

def install():
    httplib.HTTPConnection = wsgi_intercept.WSGI_HTTPConnection
    httplib.HTTPSConnection = wsgi_intercept.WSGI_HTTPSConnection

def uninstall():
    httplib.HTTPConnection = OriginalHTTPConnection
    httplib.HTTPSConnection = OriginalHTTPSConnection
