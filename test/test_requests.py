from wsgi_intercept import requests_intercept

from requests.exceptions import ConnectionError
import wsgi_intercept
from test import wsgi_app
import requests

import py.test

mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)


def install(port=80):
    requests_intercept.install()
    factory = lambda: mock_app
    wsgi_intercept.add_wsgi_intercept(
            'some_hopefully_nonexistant_domain',
            port, factory)


def uninstall():
    requests_intercept.uninstall()


def test_success():
    install()
    resp = requests.get('http://some_hopefully_nonexistant_domain:80/')
    assert resp.content == b'WSGI intercept successful!\n'
    assert mock_app.success()
    uninstall()


def test_bogus_domain():
    install()
    py.test.raises(ConnectionError,
            'requests.get("http://_nonexistant_domain_")')
    uninstall()


def test_https_success():
    install(443)
    resp = requests.get('https://some_hopefully_nonexistant_domain/')
    assert resp.content == b'WSGI intercept successful!\n'
    assert mock_app.success()
    uninstall()


def test_app_error():
    requests_intercept.install()
    port = 80
    wsgi_intercept.add_wsgi_intercept(
            'some_hopefully_nonexistant_domain',
        port, lambda: wsgi_app.raises_app)
    with py.test.raises(wsgi_intercept.WSGIAppError):
        requests.get('http://some_hopefully_nonexistant_domain:80/')
