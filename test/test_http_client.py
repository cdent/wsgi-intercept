import py.test
import wsgi_intercept
from wsgi_intercept import http_client_intercept
from test import wsgi_app
from test.install import BaseInstalledApp
try:
    import http.client as http_lib
except ImportError:
    import httplib as http_lib

HOST = 'some_hopefully_nonexistant_domain'


class InstalledApp(BaseInstalledApp):
    def install(self):
        http_client_intercept.install()
        wsgi_intercept.add_wsgi_intercept(self.host, self.port, self.factory)

    def uninstall(self):
        wsgi_intercept.remove_wsgi_intercept(self.host, self.port)
        http_client_intercept.uninstall()


def test_http_success():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_app, host=HOST, port=80) as app:
        http_client = http_lib.HTTPConnection(HOST)
        http_client.request('GET', '/')
        content = http_client.getresponse().read()
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


def test_https_success():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_app, host=HOST, port=443) as app:
        http_client = http_lib.HTTPSConnection(HOST)
        http_client.request('GET', '/')
        content = http_client.getresponse().read()
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


def test_app_error():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.raises_app)
    with InstalledApp(mock_app, host=HOST, port=80):
        http_client = http_lib.HTTPConnection(HOST)
        with py.test.raises(wsgi_intercept.WSGIAppError):
            http_client.request('GET', '/')
            http_client.getresponse().read()
