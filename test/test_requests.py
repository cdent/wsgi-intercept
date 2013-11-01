from wsgi_intercept import requests_intercept

from requests.exceptions import ConnectionError
import wsgi_intercept
from test import wsgi_app
import requests

import py.test


def install(port=80):
    requests_intercept.install()
    wsgi_intercept.add_wsgi_intercept(
            'some_hopefully_nonexistant_domain',
            port, wsgi_app.create_fn)


def uninstall():
    requests_intercept.uninstall()


def test_success():
    install()
    resp = requests.get('http://some_hopefully_nonexistant_domain:80/')
    assert resp.content == b'WSGI intercept successful!\n'
    assert wsgi_app.success()
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
    assert wsgi_app.success()
    uninstall()
