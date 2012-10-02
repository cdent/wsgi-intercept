#! /usr/bin/env python
import urllib.request
from wsgi_intercept import urllib_intercept
import wsgi_intercept
from test import wsgi_app

_saved_debuglevel = None

def add_http_intercept():
    _saved_debuglevel, wsgi_intercept.debuglevel = wsgi_intercept.debuglevel, 1
    wsgi_intercept.add_wsgi_intercept('some_hopefully_nonexistant_domain', 80, wsgi_app.create_fn)
    
def add_https_intercept():
    _saved_debuglevel, wsgi_intercept.debuglevel = wsgi_intercept.debuglevel, 1
    wsgi_intercept.add_wsgi_intercept('some_hopefully_nonexistant_domain', 443, wsgi_app.create_fn)

def remove_intercept():
    wsgi_intercept.debuglevel = _saved_debuglevel
    wsgi_intercept.remove_wsgi_intercept()

def test_http():
    add_http_intercept()
    urllib_intercept.install_opener()
    urllib.request.urlopen('http://some_hopefully_nonexistant_domain:80/')
    assert wsgi_app.success()
    remove_intercept()
    
def test_http_default_port():
    add_http_intercept()
    urllib_intercept.install_opener()
    urllib.request.urlopen('http://some_hopefully_nonexistant_domain/')
    assert wsgi_app.success()
    remove_intercept()
    
def xtest_https():
    add_https_intercept()
    urllib_intercept.install_opener()
    urllib.request.urlopen('https://some_hopefully_nonexistant_domain:443/')
    assert wsgi_app.success()
    remove_intercept()
    
def xtest_https_default_port():
    add_https_intercept()
    urllib_intercept.install_opener()
    urllib.request.urlopen('https://some_hopefully_nonexistant_domain/')
    assert wsgi_app.success()
    remove_intercept()
