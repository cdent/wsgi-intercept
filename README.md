wsgi-intercept
======================

[![travis](https://secure.travis-ci.org/cdent/wsgi-intercept.png)](https://secure.travis-ci.org/cdent/wsgi-intercept)

Documentation is available on [Read The
Docs](http://wsgi-intercept.readthedocs.org/en/latest/).

What is it?
===========

wsgi_intercept installs a WSGI application in place of a real host for
testing while still preserving HTTP semantics. See the
[PyPI page](http://pypi.python.org/pypi/wsgi_intercept) page for more details.
It works by intercepting the connection handling in http client
libraries.

Supported Libraries
-------------------

For Python 2.7 the following libraries are supported:

* `urllib2`
* `httplib`
* `httplib2`
* `requests`
* `urllib3`

In Python 3:

* `urllib.request`
* `http.client`
* `httplib2`
* `requests`
* `urllib3`

If you are using Python 2 and need support for a different HTTP
client, require a version of `wsgi_intercept<0.6`.
