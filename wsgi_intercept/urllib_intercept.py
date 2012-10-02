import sys
from wsgi_intercept import WSGI_HTTPConnection

import urllib.request, http.client
from urllib.request import HTTPHandler

class WSGI_HTTPHandler(HTTPHandler):
    """
    Override the default HTTPHandler class with one that uses the
    WSGI_HTTPConnection class to open HTTP URLs.
    """
    def http_open(self, req):
        return self.do_open(WSGI_HTTPConnection, req)

if hasattr(http.client, 'HTTPS'):
    # urllib2 did this check as well, I assume it's to see if 
    # python was compiled with SSL support
    from wsgi_intercept import WSGI_HTTPSConnection
    from urllib.request import HTTPSHandler
    
    class WSGI_HTTPSHandler(HTTPSHandler):
        """
        Override the default HTTPSHandler class with one that uses the
        WSGI_HTTPConnection class to open HTTPS URLs.
        """
        def https_open(self, req):
            return self.do_open(WSGI_HTTPSConnection, req)
else:
    WSGI_HTTPSHandler = None
    
def install_opener():
    handlers = [WSGI_HTTPHandler()]
    if WSGI_HTTPSHandler is not None:
        handlers.append(WSGI_HTTPSHandler())
    opener = urllib.request.build_opener(*handlers)
    urllib.request.install_opener(opener)

    return opener

def uninstall_opener():
    urllib.request.install_opener(None)
