import sys
import py.test
import wsgi_intercept
from wsgi_intercept import httplib2_intercept
from test import wsgi_app
from test.install import BaseInstalledApp
import httplib2

HOST = 'some_hopefully_nonexistant_domain'


class InstalledApp(BaseInstalledApp):
    def install(self):
        httplib2_intercept.install()
        wsgi_intercept.add_wsgi_intercept(
            self.host, self.port, self.factory, script_name=self.script_name)

    def uninstall(self):
        wsgi_intercept.remove_wsgi_intercept(self.host, self.port)
        httplib2_intercept.uninstall()


def test_simple_override():
    mock_simple_app = wsgi_app.MockWSGIApp(wsgi_app.simple_app)
    with InstalledApp(mock_simple_app, host=HOST) as app:
        http = httplib2.Http()
        resp, content = http.request(
            'http://some_hopefully_nonexistant_domain:80/', 'GET')
        assert app.success()


def test_more_interesting():
    mock_more_interesting_app = wsgi_app.MockWSGIApp(wsgi_app.more_interesting_app)
    with InstalledApp(mock_more_interesting_app, host=HOST) as app:
        http = httplib2.Http()
        resp, content = http.request(
            'http://some_hopefully_nonexistant_domain/%E4%B8%96%E4%B8%8A%E5%8E%9F%E4%BE%86%E9%82%84%E6%9C%89%E3%80%8C%E7%BE%9A%E7%89%9B%E3%80%8D%E9%80%99%E7%A8%AE%E5%8B%95%E7%89%A9%EF%BC%81%2Fbarney?bar=baz%20zoom',
            'GET',
            headers={'Accept': 'application/json'})
        internal_env = app.get_internals()

        assert internal_env['PATH_INFO'] == '/%E4%B8%96%E4%B8%8A%E5%8E%9F%E4%BE%86%E9%82%84%E6%9C%89%E3%80%8C%E7%BE%9A%E7%89%9B%E3%80%8D%E9%80%99%E7%A8%AE%E5%8B%95%E7%89%A9%EF%BC%81%2Fbarney'
        assert internal_env['QUERY_STRING'] == 'bar=baz%20zoom'
        assert internal_env['HTTP_ACCEPT'] == 'application/json'


def test_script_name():
    mock_more_interesting_app = wsgi_app.MockWSGIApp(wsgi_app.more_interesting_app)
    with InstalledApp(
            mock_more_interesting_app, host=HOST, script_name='/funky') as app:
        http = httplib2.Http()
        response, content = http.request(
            'http://some_hopefully_nonexistant_domain/funky/boom/baz')
        internal_env = app.get_internals()

        assert internal_env['SCRIPT_NAME'] == '/funky'
        assert internal_env['PATH_INFO'] == '/boom/baz'


@py.test.mark.xfail(
    sys.version_info[0] == 2 and sys.version_info[1] <= 6,
    reason='works okay on 2.7 and beyond. why?')
def test_encoding_errors():
    mock_more_interesting_app = wsgi_app.MockWSGIApp(wsgi_app.more_interesting_app)
    with InstalledApp(mock_more_interesting_app, host=HOST):
        http = httplib2.Http()
        with py.test.raises(UnicodeEncodeError):
            response, content = http.request(
                'http://some_hopefully_nonexistant_domain/boom/baz',
                headers={'Accept': u'application/\u2603'})
