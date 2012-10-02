import pytest
from wsgi_intercept import httplib_intercept
from socket import gaierror
import wsgi_intercept
from test import wsgi_app
import http.client

_saved_debuglevel = None


def http_install(port=80):
    _saved_debuglevel, wsgi_intercept.debuglevel = wsgi_intercept.debuglevel, 1
    httplib_intercept.install()
    wsgi_intercept.add_wsgi_intercept('some_hopefully_nonexistant_domain', port, wsgi_app.create_fn)

def http_uninstall(port=80):
    wsgi_intercept.debuglevel = _saved_debuglevel
    wsgi_intercept.remove_wsgi_intercept('some_hopefully_nonexistant_domain', port)
    httplib_intercept.uninstall()

def test_http_success():
    http_install()
    http_client = http.client.HTTPConnection('some_hopefully_nonexistant_domain')
    http_client.request('GET', '/')
    content = http_client.getresponse().read()
    assert content == b'WSGI intercept successful!\n'
    assert wsgi_app.success()
    http_uninstall()


# https and http.client are not happy because of a recursion problem
# HTTPSConnection calls super in __init__
@pytest.mark.xfail
def test_https_success():
    http_install(443)
    http_client = http.client.HTTPSConnection('some_hopefully_nonexistant_domain')
    http_client.request('GET', '/')
    content = http_client.getresponse().read()
    assert content == b'WSGI intercept successful!\n'
    assert wsgi_app.success()
    http_uninstall(443)
