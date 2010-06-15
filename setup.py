"""
TwitterLog
----------

Implements a log handler that can log to a Twitter stream.

Usage::

    import logging
    from twitterlog import TwitterHandler

    twitter = TwitterHandler('username', 'password')
    twitter.setLevel(logging.ERROR)
    logger = logging.getLogger('yourlogger')
    logger.addHandler(twitter)

Other Links
```````````

* `development version
  <http://github.com/mitsuhiko/twitterlog/zipball/master#egg=TwitterLog-dev>`_
"""
from setuptools import setup


setup(
    name='TwitterLog',
    version='0.6.1',
    url='http://github.com/mitsuhiko/twitterlog',
    license='BSD',
    author='Armin Ronacher',
    author_email='armin.ronacher@active-4.com',
    description='Implements a logging handler that logs to Twitter',
    long_description=__doc__,
    py_modules=['twitterlog'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'oauth2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
