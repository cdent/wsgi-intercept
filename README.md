python3-wsgi-intercept
======================

Python3 port of the important bits of wsgi-intercept

What is it?
===========

wsgi_intercept installs a WSGI application in place of a real URI for testing.

Introduction
------------

_This content is from the python2 version. It will be updated if
changes are made._

Testing a WSGI application normally involves starting a server at a
local host and port, then pointing your test code to that address.
Instead, this library lets you intercept calls to any specific
host/port combination and redirect them into a WSGI application
importable by your test program. Thus, you can avoid spawning multiple
processes or threads to test your Web app.

wsgi_intercept works by replacing httplib.HTTPConnection with a
subclass, wsgi_intercept.WSGI_HTTPConnection. This class then
redirects specific server/port combinations into a WSGI application by
emulating a socket. If no intercept is registered for the host and
port requested, those requests are passed on to the standard handler.

The functions add_wsgi_intercept(host, port, app_create_fn,
script_name='') and remove_wsgi_intercept(host,port) specify which
URLs should be redirect into what applications. Note especially that
app_create_fn is a function object returning a WSGI application;
script_name becomes SCRIPT_NAME in the WSGI app's environment, if set.

New Version
-----------

For the new version only basic intercept functionality will be
provided, with a working implementation for urllib.request, httplib
and httplib2. Other  frameworks later.


