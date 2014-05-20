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
        return self.app

    def __enter__(self):
        self.install()
        return self.app

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
