http_client_intercept
=====================

.. automodule:: wsgi_intercept.http_client_intercept

.. warning::

   This intercept will fail to install if you access access HTTPConnection or
   HTTPSConnection before the intercept is installed. For example, do not use
   "from http.client import HTTPConnection". Instead, "import http.client" and
   reference http.client.HTTPConnection after the intercept is installed.

Example:

.. testcode:: 

    try:
        import http.client as http_lib
    except ImportError:
        import httplib as http_lib
    from wsgi_intercept import (
        http_client_intercept, add_wsgi_intercept, remove_wsgi_intercept
    )


    def app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Whee']


    def make_app():
        return app


    host, port = 'localhost', 80
    http_client_intercept.install()
    add_wsgi_intercept(host, port, make_app)
    HTTPConnection = http_lib.HTTPConnection
    client = HTTPConnection(host)
    client.request('GET', '/')
    response = client.getresponse()
    content = response.read()
    assert content == b'Whee'
    remove_wsgi_intercept(host, port)
    http_client_intercept.uninstall()
