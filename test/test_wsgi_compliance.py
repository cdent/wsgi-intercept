from wsgi_intercept.httplib2_intercept import install, uninstall
import wsgi_intercept
from test import wsgi_app
import httplib2


_saved_debuglevel = None


def http_install():
    _saved_debuglevel, wsgi_intercept.debuglevel = wsgi_intercept.debuglevel, 1
    install()
    wsgi_intercept.add_wsgi_intercept(
            'some_hopefully_nonexistant_domain', 80, wsgi_app.create_fn)


def http_uninstall():
    wsgi_intercept.debuglevel = _saved_debuglevel
    wsgi_intercept.remove_wsgi_intercept(
            'some_hopefully_nonexistant_domain', 80)
    uninstall()


def test_simple_override():
    http_install()
    http = httplib2.Http()
    resp, content = http.request(
            'http://some_hopefully_nonexistant_domain:80/', 'GET')
    assert wsgi_app.success()
    http_uninstall()


def test_more_interesting():
    http_install()
    wsgi_intercept.add_wsgi_intercept(
            'some_hopefully_nonexistant_domain', 80,
            wsgi_app.create_mi)

    http = httplib2.Http()
    resp, content = http.request('http://some_hopefully_nonexistant_domain/%E4%B8%96%E4%B8%8A%E5%8E%9F%E4%BE%86%E9%82%84%E6%9C%89%E3%80%8C%E7%BE%9A%E7%89%9B%E3%80%8D%E9%80%99%E7%A8%AE%E5%8B%95%E7%89%A9%EF%BC%81%2Fbarney?bar=baz%20zoom',
            'GET',
            headers={'Accept': 'application/json'})
    internal_env = wsgi_app.get_internals()

    assert internal_env['PATH_INFO'] == '/%E4%B8%96%E4%B8%8A%E5%8E%9F%E4%BE%86%E9%82%84%E6%9C%89%E3%80%8C%E7%BE%9A%E7%89%9B%E3%80%8D%E9%80%99%E7%A8%AE%E5%8B%95%E7%89%A9%EF%BC%81%2Fbarney'
    assert internal_env['QUERY_STRING'] == 'bar=baz%20zoom'
    assert internal_env['HTTP_ACCEPT'] == 'application/json'

    http_uninstall()
