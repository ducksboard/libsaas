#!/usr/bin/python

"""libsaas
==========

A library to take the pain out of using SaaS APIs.

It provides an abstraction layer on top of various APIs, taking care of
constructing the URLs, serializing parameters and authentication. You just call
Python methods and receive Python objects.

It's like an ORM for SaaS!

Libsaas is built by Ducksboard_ and distributed under the MIT license. You can
file bugs in the `issue tracker`_, browse the documentation_ or help out by
constributing support for new services.

.. _Ducksboard: http://ducksboard.com/
.. _issue tracker: https://github.com/ducksboard/libsaas/issues
.. _documentation: http://docs.libsaas.net/
"""
import os
from distutils.core import setup, Command

from libsaas import __versionstr__


def abspath(path):
    return os.path.join(os.path.dirname(__file__), path)


def _is_package(path):
    if not os.path.isdir(path):
        return False
    return os.path.isfile(os.path.join(path, '__init__.py'))


def _package_name(top, path):
    path = os.path.relpath(path, abspath('.'))
    return path.replace(os.sep, '.')


def find_modules(top):
    for root, dirs, files in os.walk(abspath(top)):
        for d in dirs:
            fullpath = os.path.join(root, d)
            if not _is_package(fullpath):
                continue
            if os.path.basename(fullpath) == 'test':
                continue
            package = _package_name(top, fullpath)
            yield package
    yield top


class Test(Command):
    description = "run the automated test suite"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from test.test_libsaas import main
        main()


setup(name="libsaas",
      version=__versionstr__,
      description="Abstraction library for SaaS APIs",
      long_description=__doc__,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      platforms=["any"],
      license="MIT",
      author="Ducksboard",
      maintainer="Ducksboard",
      author_email="libsaas@ducksboard.com",
      maintainer_email="libsaas@ducksboard.com",
      url="http://libsaas.net/",
      packages=list(find_modules("libsaas")),
      scripts=["bin/saas"],
      cmdclass={'test': Test})
