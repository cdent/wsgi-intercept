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


def test_quoting_issue11():
    http_install()
    # see http://code.google.com/p/wsgi-intercept/issues/detail?id=11
    http = httplib2.Http()
    inspected_env = {}

    def make_path_checking_app():

        def path_checking_app(environ, start_response):
            inspected_env['QUERY_STRING'] = environ['QUERY_STRING']
            inspected_env['PATH_INFO'] = environ['PATH_INFO']
            status = '200 OK'
            response_headers = [('Content-type', 'text/plain')]
            start_response(status, response_headers)
            return []

        return path_checking_app

    wsgi_intercept.add_wsgi_intercept(
            'some_hopefully_nonexistant_domain', 80,
            make_path_checking_app)

    resp, content = http.request(
            'http://some_hopefully_nonexistant_domain:80/spaced+words.html?word=something%20spaced',
            'GET')

    assert ('QUERY_STRING' in inspected_env and 'PATH_INFO'
            in inspected_env), "path_checking_app() was never called?"
    assert inspected_env['PATH_INFO'] == '/spaced+words.html'
    assert inspected_env['QUERY_STRING'] == 'word=something%20spaced'
    http_uninstall()
