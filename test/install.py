class BaseInstalledApp(object):
    def __init__(self, app, host, port=80, script_name=''):
        self.app = app
        self.host = host
        self.port = port
        self.script_name = script_name

    def install(self):
        raise NotImplementedError()

    def uninstall(self):
        raise NotImplementedError()

    def factory(self):
        return self.app

    def __enter__(self):
        self.install()
        return self.app

    def __exit__(self, *args, **kwargs):
        self.uninstall()
