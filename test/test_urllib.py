import py.test
from wsgi_intercept import urllib_intercept, WSGIAppError
from test import wsgi_app
from test.install import installer_class
try:
    import urllib.request as url_lib
except ImportError:
    import urllib2 as url_lib

HOST = 'some_hopefully_nonexistant_domain'

InstalledApp = installer_class(install=urllib_intercept.install_opener)


def test_http():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=80) as app:
        url_lib.urlopen('http://some_hopefully_nonexistant_domain:80/')
        assert app.success()


def test_http_default_port():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=80) as app:
        url_lib.urlopen('http://some_hopefully_nonexistant_domain/')
        assert app.success()


def test_https():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=443) as app:
        url_lib.urlopen('https://some_hopefully_nonexistant_domain:443/')
        assert app.success()


def test_https_default_port():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=443) as app:
        url_lib.urlopen('https://some_hopefully_nonexistant_domain/')
        assert app.success()


def test_app_error():
    with InstalledApp(wsgi_app.raises_app, host=HOST, port=80):
        with py.test.raises(WSGIAppError):
            url_lib.urlopen('http://some_hopefully_nonexistant_domain:80/')
