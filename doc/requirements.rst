Requirements
============

For basic operation libsaas does not depend on any external modules, it just
uses the standard Python library. It is regularly tested on Python 2.6, 2.7,
3.2 and PyPy_.

.. _PyPy: http://pypy.org/

Optional requirements
---------------------

Some features of libsaas do need external libraries to be installed. To use one
of the pluggable executors you will need the corresponding Python module, for
instance python-requests_ for the Requests executor.

Services that use `OAuth 1.0`_ for authentication will require the
requests-oauth_ library to be installed. Note that you only need
requests-oauth_, not python-requests_ proper and that once you have it
installed, you can manipulate services that authenticate with OAuth using any
executor.

.. _python-requests: http://pypi.python.org/pypi/requests
.. _requests-oauth: http://pypi.python.org/pypi/requests-oauth
.. _OAuth 1.0: http://tools.ietf.org/html/rfc5849
