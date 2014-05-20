import py.test
from wsgi_intercept import http_client_intercept, WSGIAppError
from test import wsgi_app
from test.install import installer_class
try:
    import http.client as http_lib
except ImportError:
    import httplib as http_lib

HOST = 'some_hopefully_nonexistant_domain'

InstalledApp = installer_class(http_client_intercept)


def test_http_success():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=80) as app:
        http_client = http_lib.HTTPConnection(HOST)
        http_client.request('GET', '/')
        content = http_client.getresponse().read()
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


def test_https_success():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=443) as app:
        http_client = http_lib.HTTPSConnection(HOST)
        http_client.request('GET', '/')
        content = http_client.getresponse().read()
        assert content == b'WSGI intercept successful!\n'
        assert app.success()


def test_app_error():
    with InstalledApp(wsgi_app.raises_app, host=HOST, port=80):
        http_client = http_lib.HTTPConnection(HOST)
        with py.test.raises(WSGIAppError):
            http_client.request('GET', '/')
            http_client.getresponse().read()
