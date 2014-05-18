import py.test
import wsgi_intercept
from wsgi_intercept import urllib_intercept
from test import wsgi_app
from test.install import BaseInstalledApp
try:
    import urllib.request as url_lib
except ImportError:
    import urllib2 as url_lib

HOST = 'some_hopefully_nonexistant_domain'


class InstalledApp(BaseInstalledApp):
    def install(self):
        urllib_intercept.install_opener()
        wsgi_intercept.add_wsgi_intercept(self.host, self.port, self.factory)

    def uninstall(self):
        wsgi_intercept.remove_wsgi_intercept(self.host, self.port)


def test_http():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_app, host=HOST, port=80) as app:
        url_lib.urlopen('http://some_hopefully_nonexistant_domain:80/')
        assert app.success()


def test_http_default_port():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_app, host=HOST, port=80) as app:
        url_lib.urlopen('http://some_hopefully_nonexistant_domain/')
        assert app.success()


def test_https():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_app, host=HOST, port=443) as app:
        url_lib.urlopen('https://some_hopefully_nonexistant_domain:443/')
        assert app.success()


def test_https_default_port():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_app, host=HOST, port=443) as app:
        url_lib.urlopen('https://some_hopefully_nonexistant_domain/')
        assert app.success()


def test_app_error():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.raises_app)
    with InstalledApp(mock_app, host=HOST, port=80):
        with py.test.raises(wsgi_intercept.WSGIAppError):
            url_lib.urlopen('http://some_hopefully_nonexistant_domain:80/')
