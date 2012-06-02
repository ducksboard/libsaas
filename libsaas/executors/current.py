"""
This module holds the current executor. An executor is a function that takes a
libsaas.http.Request object and a parser function and uses them to make a HTTP
request and return a Python object result.

The current executor is a global value, set using the
libsaas.executors.base.use_executor() function. Each executor module should
expose a use() function that may take additional configuration arguments, and
it should internally call base.use_executor().

Some executors might not return the result directly, for instance the Twisted
executor returns a Deferred that fires with the result of the execution.

For information about parsers, see the docstring of libsaas.parsers.
"""


def process(request, parser):
    raise NotImplementedError("no executor in use")
