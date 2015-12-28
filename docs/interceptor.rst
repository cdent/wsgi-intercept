
Interceptor
===========

.. automodule:: wsgi_intercept.interceptor
   :members:

Example using `httplib2`, others are much the same:

.. testcode::

    import httplib2
    from wsgi_intercept.interceptor import Httplib2Interceptor


    def app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Whee']


    def make_app():
        return app


    http = httplib2.Http()
    with Httplib2Interceptor(make_app, host='localhost', port=80) as url:
        resp, content = http.request(url)
        assert content == b'Whee'
