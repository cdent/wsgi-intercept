from wsgi_intercept import httplib2_intercept
from socket import gaierror
import wsgi_intercept
from test import wsgi_app
import httplib2

import py.test


def install(port=80):
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept(
            'some_hopefully_nonexistant_domain',
            port, wsgi_app.create_fn)


def uninstall():
    httplib2_intercept.uninstall()


def test_success():
    install()
    http = httplib2.Http()
    resp, content = http.request(
            'http://some_hopefully_nonexistant_domain:80/')
    assert content == b'WSGI intercept successful!\n'
    assert wsgi_app.success()
    uninstall()


def test_bogus_domain():
    install()
    py.test.raises(gaierror,
            'httplib2_intercept.HTTP_WSGIInterceptorWithTimeout("_nonexistant_domain_").connect()')
    uninstall()


def test_https_success():
    install(443)
    http = httplib2.Http()
    resp, content = http.request('https://some_hopefully_nonexistant_domain/')
    assert wsgi_app.success()
    uninstall()
