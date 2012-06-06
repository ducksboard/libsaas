Usage
=====

To use libsaas, you first create a service object and then use the method it
provides to send and fetch data from a software as a service API.

With libsaas you always work with Python objects, serialization of data sent
and received is provided by the library. Here's an example of using libsaas to
check what's the most watched repository from all people that follow you.

.. literalinclude:: basic_example.py

Consulting original documentation
---------------------------------

The most productive way to use libsaas is to keep the original API
documentation and the libsaas documentation open side-by-side. Since every API
has its own data format, the abstraction provided by libsaas ends at providing
you with Python objects. You should refer to the original service documentation
in order to fully interpret the results.

Combining services
------------------

Libsaas is most useful when you combine access to different services. This
allows you to quickly create mashups without worrying about all the little
quirks of each API. Here's how you'd get the tickets solved yesterday in your
Zendesk and accordingly tag users who reported those tickets in Mailchimp.

You could then run this script nightly and create an automatic mailing campaign
to send quality surveys to users who's tickets have been solved recently.

.. literalinclude:: mashup_example.py

Pluggable executors
-------------------

Everything out there uses HTTP, but there's more than one way to skin a
request. By default libsaas uses Python's standard urllib2 to make HTTP
requests, but it provides a few other executor modules and you can even plug in
your own.

Here's an example of using the Requests_ executor in order to add a user agent
and a timeout every time libsaas makes a HTTP request. The example code will
unstar all gists a user has previously starred.

.. literalinclude:: requests_executor.py

Another executor included in libsaas is the Twisted_ executor that makes it
easy to integrate libsaas in Twisted programs. When using the Twisted executor,
libsaas will return Deferreds that will fire with the fetched data.

.. _Requests: http://docs.python-requests.org/
.. _Twisted: http://twistedmatrix.com/

The saas script
---------------

If you want to quickly interact with a SaaS API, you can use the `saas` command
line program. It can execute any method provided by libsaas and has some
limited discoverability features.

To use it, call it with the desired service as the first argument, followed by
the service parameters and the path to the method you want to call.

This means that code like this::

  >>> from libsaas.services import zendesk
  >>> service = zendesk.Zendesk('myapp', 'myuser', 's3cr3t')
  >>> service.user(364).tickets_requested()

Translates to::

  $ saas zendesk --subdomain=myapp --username=myuser --password=s3cr3t \
      user 364 tickets_requested

The `saas` script can also choose executors and output some debugging
information while executing::

  $ saas mailchimp --api_key=8ac789caf98879caf897a678fa76daf-us2 \
      --executor requests campaignContent 8df731

Another useful feature is that `saas` will try to interpret every parameter as
JSON, making it easier to use methods that need Python dictionaries::

  $ saas github --token_or_password=my-gh-token \
      gist 125342 update '{"description": "my gist"}'
