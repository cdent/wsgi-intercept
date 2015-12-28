"""Tests of using the context manager style.

The context manager is based on the InterceptFixture used in gabbi.
"""


import socket
from uuid import uuid4

import py.test
import requests
from httplib2 import Http, ServerNotFoundError
from six.moves import http_client
from six.moves.urllib.request import urlopen
from six.moves.urllib.error import URLError

from wsgi_intercept.interceptor import (
    Interceptor, HttpClientInterceptor, Httplib2Interceptor,
    RequestsInterceptor, UrllibInterceptor)
from .wsgi_app import simple_app


def app():
    return simple_app


# Base

def test_interceptor_instance():
    hostname = str(uuid4())
    port = 9999
    interceptor = Httplib2Interceptor(app=app, host=hostname, port=port,
                                      prefix='/foobar')
    assert isinstance(interceptor, Interceptor)
    assert interceptor.app == app
    assert interceptor.host == hostname
    assert interceptor.port == port
    assert interceptor.script_name == '/foobar'
    assert interceptor.url == 'http://%s:%s/foobar' % (hostname, port)


# http_lib

def test_httpclient_interceptor_host():
    hostname = str(uuid4())
    port = 9999
    with HttpClientInterceptor(app=app, host=hostname, port=port):
        client = http_client.HTTPConnection(hostname, port)
        client.request('GET', '/')
        response = client.getresponse()
        content = response.read().decode('utf-8')
        assert response.status == 200
        assert 'WSGI intercept successful!' in content


def test_httpclient_interceptor_url():
    hostname = str(uuid4())
    port = 9999
    url = 'http://%s:%s/' % (hostname, port)
    with HttpClientInterceptor(app=app, url=url):
        client = http_client.HTTPConnection(hostname, port)
        client.request('GET', '/')
        response = client.getresponse()
        content = response.read().decode('utf-8')
        assert response.status == 200
        assert 'WSGI intercept successful!' in content


def test_httpclient_in_out():
    hostname = str(uuid4())
    port = 9999
    url = 'http://%s:%s/' % (hostname, port)
    with HttpClientInterceptor(app=app, url=url):
        client = http_client.HTTPConnection(hostname, port)
        client.request('GET', '/')
        response = client.getresponse()
        content = response.read().decode('utf-8')
        assert response.status == 200
        assert 'WSGI intercept successful!' in content

    # outside the context manager the intercept does not work
    with py.test.raises(socket.gaierror):
        client = http_client.HTTPConnection(hostname, port)
        client.request('GET', '/')


# Httplib2

def test_httplib2_interceptor_host():
    hostname = str(uuid4())
    port = 9999
    http = Http()
    with Httplib2Interceptor(app=app, host=hostname, port=port) as url:
        response, content = http.request(url)
        assert response.status == 200
        assert 'WSGI intercept successful!' in content.decode('utf-8')


def test_httplib2_interceptor_https_host():
    hostname = str(uuid4())
    port = 443
    http = Http()
    with Httplib2Interceptor(app=app, host=hostname, port=port) as url:
        assert url == 'https://%s' % hostname
        response, content = http.request(url)
        assert response.status == 200
        assert 'WSGI intercept successful!' in content.decode('utf-8')


def test_httplib2_interceptor_no_host():
    # no hostname or port, one will be generated automatically
    # we never actually know what it is
    http = Http()
    with Httplib2Interceptor(app=app) as url:
        response, content = http.request(url)
        assert response.status == 200
        assert 'WSGI intercept successful!' in content.decode('utf-8')


def test_httplib2_interceptor_url():
    hostname = str(uuid4())
    port = 9999
    url = 'http://%s:%s/' % (hostname, port)
    http = Http()
    with Httplib2Interceptor(app=app, url=url) as target_url:
        response, content = http.request(target_url)
        assert response.status == 200
        assert 'WSGI intercept successful!' in content.decode('utf-8')


def test_httplib2_in_out():
    hostname = str(uuid4())
    port = 9999
    url = 'http://%s:%s/' % (hostname, port)
    http = Http()
    with Httplib2Interceptor(app=app, url=url) as target_url:
        response, content = http.request(target_url)
        assert response.status == 200
        assert 'WSGI intercept successful!' in content.decode('utf-8')

    # outside the context manager the intercept does not work
    with py.test.raises(ServerNotFoundError):
        http.request(url)


# Requests

def test_requests_interceptor_host():
    hostname = str(uuid4())
    port = 9999
    with RequestsInterceptor(app=app, host=hostname, port=port) as url:
        response = requests.get(url)
        assert response.status_code == 200
        assert 'WSGI intercept successful!' in response.text


def test_requests_interceptor_url():
    hostname = str(uuid4())
    port = 9999
    url = 'http://%s:%s/' % (hostname, port)
    with RequestsInterceptor(app=app, url=url) as target_url:
        response = requests.get(target_url)
        assert response.status_code == 200
        assert 'WSGI intercept successful!' in response.text


def test_requests_in_out():
    hostname = str(uuid4())
    port = 9999
    url = 'http://%s:%s/' % (hostname, port)
    with RequestsInterceptor(app=app, url=url) as target_url:
        response = requests.get(target_url)
        assert response.status_code == 200
        assert 'WSGI intercept successful!' in response.text

    # outside the context manager the intercept does not work
    with py.test.raises(requests.ConnectionError):
        requests.get(url)


# urllib

def test_urllib_interceptor_host():
    hostname = str(uuid4())
    port = 9999
    with UrllibInterceptor(app=app, host=hostname, port=port) as url:
        response = urlopen(url)
        assert response.code == 200
        assert 'WSGI intercept successful!' in response.read().decode('utf-8')


def test_urllib_interceptor_url():
    hostname = str(uuid4())
    port = 9999
    url = 'http://%s:%s/' % (hostname, port)
    with UrllibInterceptor(app=app, url=url) as target_url:
        response = urlopen(target_url)
        assert response.code == 200
        assert 'WSGI intercept successful!' in response.read().decode('utf-8')


def test_urllib_in_out():
    hostname = str(uuid4())
    port = 9999
    url = 'http://%s:%s/' % (hostname, port)
    with UrllibInterceptor(app=app, url=url) as target_url:
        response = urlopen(target_url)
        assert response.code == 200
        assert 'WSGI intercept successful!' in response.read().decode('utf-8')

    # outside the context manager the intercept does not work
    with py.test.raises(URLError):
        urlopen(url)
