"""Intercept HTTP connections that use `mechanize <http://wwwsearch.sourceforge.net/mechanize/>`_.
"""
import sys
import platform
assert sys.version_info < (3, 0), "mechanize cannot be installed in Python 3"
assert platform.python_implementation() != "PyPy", (
    "mechanize does not import on PyPy"
)
import mechanize
from wsgi_intercept.urllib_intercept import WSGI_HTTPHandler, WSGI_HTTPSHandler


_ORIGINAL_BROWSER = mechanize.Browser


class Browser(_ORIGINAL_BROWSER):
    """mechanize Browser class with our WSGI intercept handlers installed.
    """
    handler_classes = _ORIGINAL_BROWSER.handler_classes.copy()
    handler_classes['http'] = WSGI_HTTPHandler
    handler_classes['https'] = WSGI_HTTPSHandler

    def __init__(self, *args, **kwargs):
        _ORIGINAL_BROWSER.__init__(self, *args, **kwargs)


def install():
    mechanize.Browser = Browser


def uninstall():
    if mechanize.Browser == Browser:
        mechanize.Browser = _ORIGINAL_BROWSER
