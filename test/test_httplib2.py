import py.test
from wsgi_intercept import httplib2_intercept, WSGIAppError
from test import wsgi_app
from test.install import installer_class
import httplib2
from socket import gaierror

HOST = 'some_hopefully_nonexistant_domain'

InstalledApp = installer_class(httplib2_intercept)


def test_success():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=80) as app:
        http = httplib2.Http()
        resp, content = http.request(
            'http://some_hopefully_nonexistant_domain:80/')
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


def test_bogus_domain():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=80):
        py.test.raises(
            gaierror,
            'httplib2_intercept.HTTP_WSGIInterceptorWithTimeout("_nonexistant_domain_").connect()')


def test_https_success():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=443) as app:
        http = httplib2.Http()
        resp, content = http.request('https://some_hopefully_nonexistant_domain/')
        assert app.success()


def test_app_error():
    with InstalledApp(wsgi_app.raises_app, host=HOST, port=80):
        http = httplib2.Http()
        with py.test.raises(WSGIAppError):
            http.request(
                'http://some_hopefully_nonexistant_domain:80/')
