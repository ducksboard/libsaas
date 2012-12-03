=======================
 libsaas documentation
=======================

Libsaas is a Python library that makes it easy to interact with various
software as a service APIs. Think of it as an ORM for APIs.

Libsaas handles all the nitty-gritty details, such as input and output format,
authentication and URL schemes. You don't have to deal with serialization,
extra headers and other quirks of various APIs. Everything's Python, you just
pass Python objects to Python functions and get the results out::

  >>> from libsaas.services import zendesk
  >>> service = zendesk.Zendesk('myapp', 'myuser', 's3cr3t')
  >>> joe = service.users().search('joe@example.org')['users'][0]
  >>> joes_tickets = service.user(joe['id']).tickets_requested()
  >>> for ticket in joes_tickets:
  ...    print(ticket['description'])

Check out the list of currently supported services, add your own connectors and
help us make using APIs less painful!

.. toctree::
    :maxdepth: 2

    requirements
    usage
    unicode
    generated/services

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. image:: https://secure.travis-ci.org/ducksboard/libsaas.png?branch=master
