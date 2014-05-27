import sys
import platform
import py.test
from wsgi_intercept import WSGIAppError
from test import wsgi_app
from test.install import installer_class
try:
    import urllib.request as url_lib
except ImportError:
    import urllib2 as url_lib


# Without this conditional, the import of mechanize_intercept attempts
# to import mechanize, which cannot be installed on Python3 and throws
# exceptions on PyPy, resulting in a spurious error during test
# collection.
CAN_RUN_TESTS = (
    sys.version_info < (3, 0) and platform.python_implementation() != 'PyPy'
)
if CAN_RUN_TESTS:
    from wsgi_intercept import mechanize_intercept
    import mechanize
    InstalledApp = installer_class(mechanize_intercept)
else:
    InstalledApp = None


HOST = 'some_hopefully_nonexistent_domain'

ONLY_PYTHON2_NOT_PYPY = py.test.mark.skipif(not CAN_RUN_TESTS,
    reason="mechanize is not ported from Python 2 and fails in PyPy"
)


@ONLY_PYTHON2_NOT_PYPY
def test_success():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=80) as app:
        browser = mechanize.Browser()
        url = 'http://some_hopefully_nonexistent_domain'
        response = browser.open(url)
        content = response.read()
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


@ONLY_PYTHON2_NOT_PYPY
def test_bogus_domain():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=80):
        browser = mechanize.Browser()
        with py.test.raises(url_lib.URLError):
            browser.open('https://_nonexistent_domain')


@ONLY_PYTHON2_NOT_PYPY
def test_https_success():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=443) as app:
        browser = mechanize.Browser()
        response = browser.open('https://some_hopefully_nonexistent_domain')
        content = response.read()
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


@ONLY_PYTHON2_NOT_PYPY
def test_app_error():
    with InstalledApp(wsgi_app.raises_app, host=HOST, port=80):
        with py.test.raises(WSGIAppError):
            browser = mechanize.Browser()
            response = browser.open('http://some_hopefully_nonexistent_domain')
            response.read()
