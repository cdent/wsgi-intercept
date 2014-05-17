urllib_intercept
================

.. automodule:: wsgi_intercept.urllib_intercept


Example:

.. testcode:: 

    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen
    from wsgi_intercept import (
        urllib_intercept, add_wsgi_intercept, remove_wsgi_intercept
    )


    def app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Whee']


    def make_app():
        return app


    host, port = 'localhost', 80
    url = 'http://{0}:{1}/'.format(host, port)
    urllib_intercept.install_opener()
    add_wsgi_intercept(host, port, make_app)
    stream = urlopen(url)
    content = stream.read()
    assert content == b'Whee'
    remove_wsgi_intercept()
