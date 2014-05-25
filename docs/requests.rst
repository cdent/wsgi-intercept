requests_intercept
==================

.. automodule:: wsgi_intercept.requests_intercept


Example:

.. testcode:: 

    import requests
    from wsgi_intercept import requests_intercept, add_wsgi_intercept


    def app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Whee']


    def make_app():
        return app


    host, port = 'localhost', 80
    url = 'http://{0}:{1}/'.format(host, port)
    requests_intercept.install()
    add_wsgi_intercept(host, port, make_app)
    resp = requests.get(url)
    assert resp.content == b'Whee'
    requests_intercept.uninstall()
