try:
    import urllib.request as url_lib
except ImportError:
    import urllib2 as url_lib
import py.test
from wsgi_intercept import urllib_intercept
import wsgi_intercept
from test import wsgi_app


mock_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)


def add_http_intercept(port=80):
    factory = lambda: mock_app
    wsgi_intercept.add_wsgi_intercept(
            'some_hopefully_nonexistant_domain',
            port, factory)


def remove_intercept():
    wsgi_intercept.remove_wsgi_intercept()


def test_http():
    add_http_intercept()
    urllib_intercept.install_opener()
    url_lib.urlopen('http://some_hopefully_nonexistant_domain:80/')
    assert mock_app.success()
    remove_intercept()


def test_http_default_port():
    add_http_intercept()
    urllib_intercept.install_opener()
    url_lib.urlopen('http://some_hopefully_nonexistant_domain/')
    assert mock_app.success()
    remove_intercept()


def test_https():
    add_http_intercept(443)
    urllib_intercept.install_opener()
    url_lib.urlopen('https://some_hopefully_nonexistant_domain:443/')
    assert mock_app.success()
    remove_intercept()


def test_https_default_port():
    add_http_intercept(443)
    urllib_intercept.install_opener()
    url_lib.urlopen('https://some_hopefully_nonexistant_domain/')
    assert mock_app.success()
    remove_intercept()


def test_app_error():
    port = 80
    wsgi_intercept.add_wsgi_intercept(
        'some_hopefully_nonexistant_domain',
        port, lambda: wsgi_app.raises_app)
    urllib_intercept.install_opener()
    with py.test.raises(wsgi_intercept.WSGIAppError):
        url_lib.urlopen('http://some_hopefully_nonexistant_domain:80/')
