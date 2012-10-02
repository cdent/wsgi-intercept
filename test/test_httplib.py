#! /usr/bin/env python2.4
from wsgi_intercept import httplib_intercept
from socket import gaierror
import wsgi_intercept
from test import wsgi_app
import http.client

_saved_debuglevel = None


def http_install():
    _saved_debuglevel, wsgi_intercept.debuglevel = wsgi_intercept.debuglevel, 1
    httplib_intercept.install()
    wsgi_intercept.add_wsgi_intercept('some_hopefully_nonexistant_domain', 80, wsgi_app.create_fn)

def http_uninstall():
    wsgi_intercept.debuglevel = _saved_debuglevel
    wsgi_intercept.remove_wsgi_intercept('some_hopefully_nonexistant_domain', 80)
    httplib_intercept.uninstall()

def test_http_success():
    http_install()
    http_client = http.client.HTTPConnection('some_hopefully_nonexistant_domain')
    http_client.request('GET', '/')
    content = http_client.getresponse().read()
    assert content is 'WSGI intercept successful!\n'
    assert wsgi_app.success()
    http_uninstall()



def https_install():
    _saved_debuglevel, wsgi_intercept.debuglevel = wsgi_intercept.debuglevel, 1
    httplib_intercept.install()
    wsgi_intercept.add_wsgi_intercept('some_hopefully_nonexistant_domain', 443, wsgi_app.create_fn)

def https_uninstall():
    wsgi_intercept.debuglevel = _saved_debuglevel
    wsgi_intercept.remove_wsgi_intercept('some_hopefully_nonexistant_domain', 443)
    httplib_intercept.uninstall()
    
def test_https_success():
    https_install()
    http = httplib.HTTPSConnection('some_hopefully_nonexistant_domain')
    http.request('GET', '/')
    content = http.getresponse().read()
    eq_(content, 'WSGI intercept successful!\n')
    assert wsgi_app.success()
    https_uninstall()
