
from setuptools import setup, find_packages

setup(
    name = 'wsgi_intercept',
    version = '0.1',
    author = 'Titus Brown, Kumar McMillan, Chris Dent',
    author_email = 'cdent@peermore.com',
    description = 'wsgi_intercept installs a WSGI application in place of a real URI for testing.',
    # What will the name be?
    #url="http://pypi.python.org/pypi/wsgi_intercept",
    long_description = open('README.md').read(),
    license = 'MIT License',
    packages = find_packages(),
    )
