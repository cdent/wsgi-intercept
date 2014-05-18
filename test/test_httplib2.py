import py.test
import wsgi_intercept
from wsgi_intercept import httplib2_intercept
from test import wsgi_app
from test.install import BaseInstalledApp
import httplib2
from socket import gaierror

HOST = 'some_hopefully_nonexistant_domain'


class InstalledApp(BaseInstalledApp):
    def install(self):
        httplib2_intercept.install()
        wsgi_intercept.add_wsgi_intercept(self.host, self.port, self.factory)

    def uninstall(self):
        wsgi_intercept.remove_wsgi_intercept(self.host, self.port)
        httplib2_intercept.uninstall()


def test_success():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_app, host=HOST, port=80) as app:
        http = httplib2.Http()
        resp, content = http.request(
            'http://some_hopefully_nonexistant_domain:80/')
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


def test_bogus_domain():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_app, host=HOST, port=80):
        py.test.raises(
            gaierror,
            'httplib2_intercept.HTTP_WSGIInterceptorWithTimeout("_nonexistant_domain_").connect()')


def test_https_success():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_app, host=HOST, port=443) as app:
        http = httplib2.Http()
        resp, content = http.request('https://some_hopefully_nonexistant_domain/')
        assert app.success()


def test_app_error():
    mock_app = wsgi_app.MockWSGIApp(wsgi_app.raises_app)
    with InstalledApp(mock_app, host=HOST, port=80):
        http = httplib2.Http()
        with py.test.raises(wsgi_intercept.WSGIAppError):
            http.request(
                'http://some_hopefully_nonexistant_domain:80/')
