import wsgi_intercept


class BaseInstalledApp(object):
    def __init__(self, app, host, port=80, script_name='',
                 install=None, uninstall=None):
        self.app = app
        self.host = host
        self.port = port
        self.script_name = script_name
        self._install = install or (lambda: None)
        self._uninstall = uninstall or (lambda: None)
        self._hits = 0
        self._internals = {}

    def __call__(self, environ, start_response):
        self._hits += 1
        self._internals = environ
        return self.app(environ, start_response)

    def success(self):
        return self._hits > 0

    def get_internals(self):
        return self._internals

    def install_wsgi_intercept(self):
        wsgi_intercept.add_wsgi_intercept(
            self.host, self.port, self.factory, script_name=self.script_name)

    def uninstall_wsgi_intercept(self):
        wsgi_intercept.remove_wsgi_intercept(self.host, self.port)

    def install(self):
        self._install()
        self.install_wsgi_intercept()

    def uninstall(self):
        self.uninstall_wsgi_intercept()
        self._uninstall()

    def factory(self):
        return self

    def __enter__(self):
        self.install()
        return self

    def __exit__(self, *args, **kwargs):
        self.uninstall()


def installer_class(module=None, install=None, uninstall=None):
    if module:
        install = install or getattr(module, 'install', None)
        uninstall = uninstall or getattr(module, 'uninstall', None)

    class InstalledApp(BaseInstalledApp):
        def __init__(self, app, host, port=80, script_name=''):
            BaseInstalledApp.__init__(
                self, app=app, host=host, port=port, script_name=script_name,
                install=install, uninstall=uninstall)

    return InstalledApp
