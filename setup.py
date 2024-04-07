
from setuptools import setup, find_packages

VERSION = '1.13.0'

CLASSIFIERS = """
Environment :: Web Environment
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python :: 3
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3.12
Topic :: Internet :: WWW/HTTP :: WSGI
Topic :: Software Development :: Testing
""".strip().splitlines()


META = {
    'name': 'wsgi_intercept',
    'version': VERSION,
    'author': 'Titus Brown, Kumar McMillan, Chris Dent, Sasha Hart',
    'author_email': 'cdent@peermore.com',
    'description':
        'wsgi_intercept installs a WSGI application in place of a '
        'real URI for testing.',
    # What will the name be?
    'url': 'http://pypi.python.org/pypi/wsgi_intercept',
    'long_description': open('README').read(),
    'license': 'MIT License',
    'classifiers': CLASSIFIERS,
    'packages': find_packages(),
    'python_requires': '>=3',
    'extras_require': {
        'testing': [
            'pytest>=2.4',
            'httplib2',
            'requests>=2.0.1',
            'urllib3>=2.0.0',
        ],
        'docs': [
            'sphinx',
        ],
    },
}

if __name__ == '__main__':
    setup(**META)
