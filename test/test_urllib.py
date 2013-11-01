try:
    import urllib.request as url_lib
except ImportError:
    import urllib2 as url_lib
from wsgi_intercept import urllib_intercept
import wsgi_intercept
from test import wsgi_app


def add_http_intercept(port=80):
    wsgi_intercept.add_wsgi_intercept(
            'some_hopefully_nonexistant_domain',
            port, wsgi_app.create_fn)


def remove_intercept():
    wsgi_intercept.remove_wsgi_intercept()


def test_http():
    add_http_intercept()
    urllib_intercept.install_opener()
    url_lib.urlopen('http://some_hopefully_nonexistant_domain:80/')
    assert wsgi_app.success()
    remove_intercept()


def test_http_default_port():
    add_http_intercept()
    urllib_intercept.install_opener()
    url_lib.urlopen('http://some_hopefully_nonexistant_domain/')
    assert wsgi_app.success()
    remove_intercept()


def test_https():
    add_http_intercept(443)
    urllib_intercept.install_opener()
    url_lib.urlopen('https://some_hopefully_nonexistant_domain:443/')
    assert wsgi_app.success()
    remove_intercept()


def test_https_default_port():
    add_http_intercept(443)
    urllib_intercept.install_opener()
    url_lib.urlopen('https://some_hopefully_nonexistant_domain/')
    assert wsgi_app.success()
    remove_intercept()
