from wsgi_intercept import http_client_intercept
import wsgi_intercept
from test import wsgi_app

try:
    import http.client as http_lib
except ImportError:
    import httplib as http_lib


def teardown_module():
    """Ensure overrides removed."""
    http_uninstall(443)
    http_uninstall(80)


def http_install(port=80):
    http_client_intercept.install()
    wsgi_intercept.add_wsgi_intercept(
            'some_hopefully_nonexistant_domain', port, wsgi_app.create_fn)


def http_uninstall(port=80):
    wsgi_intercept.remove_wsgi_intercept(
            'some_hopefully_nonexistant_domain', port)
    http_client_intercept.uninstall()


def test_http_success():
    http_install()
    http_client = http_lib.HTTPConnection(
            'some_hopefully_nonexistant_domain')
    http_client.request('GET', '/')
    content = http_client.getresponse().read()
    assert content == b'WSGI intercept successful!\n'
    assert wsgi_app.success()
    http_uninstall()


def test_https_success():
    http_install(443)
    http_client = http_lib.HTTPSConnection(
            'some_hopefully_nonexistant_domain')
    http_client.request('GET', '/')
    content = http_client.getresponse().read()
    assert content == b'WSGI intercept successful!\n'
    assert wsgi_app.success()
    http_uninstall(443)
