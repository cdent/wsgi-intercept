"""Context manager based interception."""

from importlib import import_module

from six.moves.urllib import parse as urlparse

import wsgi_intercept


class Interceptor(object):

    def __init__(self, app, host=None, port=None, prefix=None, url=None):
        assert app
        assert (host and port) or (url)

        self.app = app

        if url:
            self._init_from_url(url)
        else:
            self.host = host
            self.port = int(port)
            self.script_name = prefix or ''

        self._module = import_module('.%s' % self.MODULE_NAME,
                                     package='wsgi_intercept')

    def __enter__(self):
        self._install_intercept()
        wsgi_intercept.add_wsgi_intercept(self.host, self.port, self.app,
                                          script_name=self.script_name)

    def __exit__(self, exc_type, value, traceback):
        wsgi_intercept.remove_wsgi_intercept(self.host, self.port)
        self._uninstall_intercept()

    def _init_from_url(self, url):
        parsed_url = urlparse.urlsplit(url)
        host, port = parsed_url.netloc.split(':')
        if not port:
            if parsed_url.scheme == 'https':
                port = 443
            else:
                port = 80
        path = parsed_url.path
        if path == '/' or not path:
            self.script_name = ''
        else:
            self.script_name = path
        self.host = host
        self.port = int(port)

    def _install_intercept(self):
        self._module.install()

    def _uninstall_intercept(self):
        self._module.uninstall()


class HttpClientInterceptor(Interceptor):

    MODULE_NAME = 'http_client_intercept'


class Httplib2Interceptor(Interceptor):

    MODULE_NAME = 'httplib2_intercept'


class RequestsInterceptor(Interceptor):

    MODULE_NAME = 'requests_intercept'


class UrllibInterceptor(Interceptor):

    MODULE_NAME = 'urllib_intercept'
