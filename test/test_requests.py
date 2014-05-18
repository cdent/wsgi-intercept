import py.test
import wsgi_intercept
from wsgi_intercept import requests_intercept
from test import wsgi_app
from test.install import BaseInstalledApp
import requests
from requests.exceptions import ConnectionError

HOST = 'some_hopefully_nonexistant_domain'


class InstalledApp(BaseInstalledApp):
    def install(self):
        requests_intercept.install()
        wsgi_intercept.add_wsgi_intercept(self.host, self.port, self.factory)

    def uninstall(self):
        requests_intercept.uninstall()


def test_success():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_app, host=HOST, port=80) as app:
        resp = requests.get('http://some_hopefully_nonexistant_domain:80/')
        assert resp.content == b'WSGI intercept successful!\n'
        assert app.success()


def test_bogus_domain():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_app, host=HOST, port=80):
        py.test.raises(
            ConnectionError,
            'requests.get("http://_nonexistant_domain_")')


def test_https_success():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_app, host=HOST, port=443) as app:
        resp = requests.get('https://some_hopefully_nonexistant_domain/')
        assert resp.content == b'WSGI intercept successful!\n'
        assert app.success()


def test_app_error():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.raises_app)
    with InstalledApp(mock_app, host=HOST, port=80):
        with py.test.raises(wsgi_intercept.WSGIAppError):
            requests.get('http://some_hopefully_nonexistant_domain:80/')
