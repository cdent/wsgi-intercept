"""Context manager based interception."""

from importlib import import_module

from six.moves.urllib import parse as urlparse

import wsgi_intercept


class Interceptor(object):

    def __init__(self, app, host=None, port=80, prefix=None, url=None):
        assert app
        assert (host and port) or (url)

        self.app = app

        if url:
            self._init_from_url(url)
            self.url = url
        else:
            self.host = host
            self.port = int(port)
            self.script_name = prefix or '/'
            self.url = self._url_from_primitives()

        self._module = import_module('.%s' % self.MODULE_NAME,
                                     package='wsgi_intercept')

    def __enter__(self):
        self.install_intercept()
        return self.url

    def __exit__(self, exc_type, value, traceback):
        self.uninstall_intercept()

    def _url_from_primitives(self):
        if self.port == 443:
            scheme = 'https'
        else:
            scheme = 'http'

        if self.port and self.port not in [443, 80]:
            port = ':%s' % self.port
        else:
            port = ''
        netloc = self.host + port

        return urlparse.urlunsplit((scheme, netloc, self.script_name, None, None))

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

    def install_intercept(self):
        self._module.install()
        wsgi_intercept.add_wsgi_intercept(self.host, self.port, self.app,
                                          script_name=self.script_name)

    def uninstall_intercept(self):
        wsgi_intercept.remove_wsgi_intercept(self.host, self.port)
        self._module.uninstall()


class HttpClientInterceptor(Interceptor):

    MODULE_NAME = 'http_client_intercept'


class Httplib2Interceptor(Interceptor):

    MODULE_NAME = 'httplib2_intercept'


class RequestsInterceptor(Interceptor):

    MODULE_NAME = 'requests_intercept'


class UrllibInterceptor(Interceptor):

    MODULE_NAME = 'urllib_intercept'
