httplib2_intercept
==================

.. automodule:: wsgi_intercept.httplib2_intercept

Example:

.. testcode:: 

    import httplib2
    from wsgi_intercept import httplib2_intercept, add_wsgi_intercept


    def app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Whee']


    def make_app():
        return app


    host, port = 'localhost', 80
    url = 'http://{0}:{1}/'.format(host, port)
    httplib2_intercept.install()
    add_wsgi_intercept(host, port, make_app)
    http = httplib2.Http()
    resp, content = http.request(url)
    assert content == b'Whee'
    httplib2_intercept.uninstall()
