urllib3_intercept
==================

.. automodule:: wsgi_intercept.urllib3_intercept


Example:

.. testcode:: 

    import urllib3
    from wsgi_intercept import urllib3_intercept, add_wsgi_intercept

    pool = urllib3.PoolManager()


    def app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Whee']


    def make_app():
        return app


    host, port = 'localhost', 80
    url = 'http://{0}:{1}/'.format(host, port)
    urllib3_intercept.install()
    add_wsgi_intercept(host, port, make_app)
    resp = pool.requests('GET', url)
    assert resp.data == b'Whee'
    urllib3_intercept.uninstall()
