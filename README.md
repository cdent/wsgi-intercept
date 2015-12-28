python3-wsgi-intercept
======================

[![travis](https://secure.travis-ci.org/cdent/python3-wsgi-intercept.png)](https://secure.travis-ci.org/cdent/python3-wsgi-intercept)

Python3 port of the important bits of wsgi-intercept, now working for
2.7, 3.3, 3.4 and 3.5.

Documentation is available on [Read The
Docs](http://wsgi-intercept.readthedocs.org/en/latest/).

What is it?
===========

wsgi_intercept installs a WSGI application in place of a real host for
testing while still preserving HTTP semantics. See the
[PyPI page](http://pypi.python.org/pypi/wsgi_intercept) page for more details.

Modern Version
-----------

For the 2 and 3 version only some intercept functionality is provided,
with a working implementation in Python 2 for:

* `urllib2`
* `httplib`
* `httplib2`
* `requests`

and in Python 3 for:

* `urllib.request`
* `http.client`
* `httplib2`
* `requests`

If you are using Python 2 and need support for a different HTTP
client, require a version of `wsgi_intercept<0.6`. Another option
to keep in mind is that interceptor code from earlier versions,
such as the interceptor for `mechanize` ought to work when imported
independently (see [related
conversation](https://github.com/cdent/wsgi-intercept/issues/16)).
