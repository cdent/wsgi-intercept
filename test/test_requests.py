import py.test
from wsgi_intercept import requests_intercept, WSGIAppError
from test import wsgi_app
from test.install import installer_class
import requests
from requests.exceptions import ConnectionError

HOST = 'some_hopefully_nonexistant_domain'

InstalledApp = installer_class(requests_intercept)


def test_success():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=80) as app:
        resp = requests.get('http://some_hopefully_nonexistant_domain:80/')
        assert resp.content == b'WSGI intercept successful!\n'
        assert app.success()


def test_bogus_domain():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=80):
        py.test.raises(
            ConnectionError,
            'requests.get("http://_nonexistant_domain_")')


def test_https_success():
    with InstalledApp(wsgi_app.simple_app, host=HOST, port=443) as app:
        resp = requests.get('https://some_hopefully_nonexistant_domain/')
        assert resp.content == b'WSGI intercept successful!\n'
        assert app.success()


def test_app_error():
    with InstalledApp(wsgi_app.raises_app, host=HOST, port=80):
        with py.test.raises(WSGIAppError):
            requests.get('http://some_hopefully_nonexistant_domain:80/')


def test_http_not_intercepted():
    with InstalledApp(wsgi_app.raises_app, host=HOST, port=80):
        resp = requests.get("http://google.com")
        assert resp.status_code >= 200 and resp.status_code < 300


def test_https_not_intercepted():
    with InstalledApp(wsgi_app.raises_app, host=HOST, port=80):
        resp = requests.get("https://google.com")
        assert resp.status_code >= 200 and resp.status_code < 300
