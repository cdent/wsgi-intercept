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


CAN_RUN_MECHANIZE = (
    sys.version_info < (3, 0) and platform.python_implementation() != 'PyPy'
)
if CAN_RUN_MECHANIZE:
    try:
        from wsgi_intercept import mechanize_intercept
        import mechanize
        InstalledApp = installer_class(mechanize_intercept)
    except ImportError:
        mechanize = None
else:
    mechanize = None


HOST = 'some_hopefully_nonexistent_domain'

SKIP_WITHOUT_MECHANIZE = py.test.mark.skipif(
    not CAN_RUN_MECHANIZE or not mechanize,
    reason="testing mechanize requires it to be installed, "
           "and mechanize cannot run on Python3 or PyPy"
)


@SKIP_WITHOUT_MECHANIZE
def test_http():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=80) as app:
        browser = mechanize.Browser()
        url = 'http://some_hopefully_nonexistent_domain:80'
        response = browser.open(url)
        content = response.read()
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


@SKIP_WITHOUT_MECHANIZE
def test_http_default_port():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=80) as app:
        browser = mechanize.Browser()
        url = 'http://some_hopefully_nonexistent_domain'
        response = browser.open(url)
        content = response.read()
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


@SKIP_WITHOUT_MECHANIZE
def test_http_other_port():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=8080) as app:
        browser = mechanize.Browser()
        url = 'http://some_hopefully_nonexistent_domain:8080'
        response = browser.open(url)
        content = response.read()
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


@SKIP_WITHOUT_MECHANIZE
def test_bogus_domain():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=80):
        browser = mechanize.Browser()
        with py.test.raises(url_lib.URLError):
            browser.open('https://_nonexistent_domain')


@SKIP_WITHOUT_MECHANIZE
def test_https():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=443) as app:
        browser = mechanize.Browser()
        response = browser.open('https://some_hopefully_nonexistent_domain')
        content = response.read()
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


@SKIP_WITHOUT_MECHANIZE
def test_https_default_port():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=443) as app:
        browser = mechanize.Browser()
        response = browser.open('https://some_hopefully_nonexistent_domain:443')
        content = response.read()
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


@SKIP_WITHOUT_MECHANIZE
def test_app_error():
    with InstalledApp(wsgi_app.raises_app, host=HOST, port=80):
        with py.test.raises(WSGIAppError):
            browser = mechanize.Browser()
            response = browser.open('http://some_hopefully_nonexistent_domain')
            response.read()
