"""Tests of using the context manager style.

The context manager is based on the InterceptFixture used in gabbi.
"""


from uuid import uuid4

import py.test
import requests
from httplib2 import Http, ServerNotFoundError

from wsgi_intercept.interceptor import Interceptor, Httplib2Interceptor, RequestsInterceptor
from .wsgi_app import simple_app

def app():
    return simple_app

def test_interceptor_instance():
    hostname = str(uuid4())
    port = 9999
    interceptor = Httplib2Interceptor(app=app, host=hostname, port=port)
    assert isinstance(interceptor, Interceptor)
    assert interceptor.app == app
    assert interceptor.host == hostname
    assert interceptor.port == port
    assert interceptor.script_name == ''


def test_httplib2_interceptor_host():
    hostname = str(uuid4())
    port = 9999
    http = Http()
    with Httplib2Interceptor(app=app, host=hostname, port=port):
        url = 'http://%s:%s/' % (hostname, port)
        response, content = http.request(url)
        assert response.status == 200
        assert 'WSGI intercept successful!' in content.decode('utf-8')


def test_httplib2_interceptor_url():
    hostname = str(uuid4())
    port = 9999
    url = 'http://%s:%s/' % (hostname, port)
    http = Http()
    with Httplib2Interceptor(app=app, url=url):
        response, content = http.request(url)
        assert response.status == 200
        assert 'WSGI intercept successful!' in content.decode('utf-8')


def test_httplib2():
    hostname = str(uuid4())
    port = 9999
    url = 'http://%s:%s/' % (hostname, port)
    http = Http()
    with Httplib2Interceptor(app=app, url=url):
        response, content = http.request(url)
        assert response.status == 200
        assert 'WSGI intercept successful!' in content.decode('utf-8')

    # outside the context manager the intercept does not work
    with py.test.raises(ServerNotFoundError):
        http.request(url)

def test_requests_interceptor_host():
    hostname = str(uuid4())
    port = 9999
    http = Http()
    with RequestsInterceptor(app=app, host=hostname, port=port):
        url = 'http://%s:%s/' % (hostname, port)
        response = requests.get(url)
        assert response.status_code == 200
        assert 'WSGI intercept successful!' in response.text


def test_requests_interceptor_url():
    hostname = str(uuid4())
    port = 9999
    url = 'http://%s:%s/' % (hostname, port)
    with RequestsInterceptor(app=app, url=url):
        response = requests.get(url)
        assert response.status_code == 200
        assert 'WSGI intercept successful!' in response.text

def test_requests_in_out():
    hostname = str(uuid4())
    port = 9999
    url = 'http://%s:%s/' % (hostname, port)
    with RequestsInterceptor(app=app, url=url):
        response = requests.get(url)
        assert response.status_code == 200
        assert 'WSGI intercept successful!' in response.text

    # outside the context manager the intercept does not work
    with py.test.raises(requests.ConnectionError):
        requests.get(url)
