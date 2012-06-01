Unicode support
===============

Libsaas supports both 2.x and 3.x versions of Python, so some rules about where
to use Unicode and where to use byte strings need to be followed.

As defined in the standards, URLs are ASCII-only. Characters from outside of
ASCII should be encoded using so-called percent encoding. Encoding schemes,
such as UTF-8 or ISO-8859-2 are mostly outside of the scope of HTTP. Libsaas
tries to be flexible in what it accepts as user input and handles encoding and
percent quoting automatically for you.

When you pass a string parameter to a libsaas method, it will be coerced to
bytes before percent-encoding, and UTF-8 will be used as the encoding. This
means that in Python 2 parameters of the `str` type will be used as-is and
`unicode` parameters will be encoded according to UTF-8. In Python 3 `str`
parameters will be UTF-8 encoded and `bytes` will be used as-is.

If you need to send characters outside of ASCII in different encoding than
UTF-8, encode them yourself and hand the bytes off to libsaas.

Data returned from libsaas methods might be encoded differently, depending on
the method in question. For most APIs using JSON it will be Unicode, because the
JSON standard mandates the use of UTF-8, making it easy to convert bytes
received from the service into Unicode characters. Some APIs though might
return binary data, such as APIs exporting images or providing access to raw
files. When in doubt, consult the upstream service documentation.

Internal usage
~~~~~~~~~~~~~~

This section is only relevant if you are extending libsaas. Normal users that
only interact with libsaas via the methods it provides can safely skip it.

Internally, libsaas uses a structure called :class:`Request` to prepare and
execute a HTTP request. There are four pieces of information this structure
holds:

 * the HTTP method to use
 * the URL (without query parameters)
 * the query parameters
 * HTTP headers

Here's how each of them should be represented with regards to Unicode/bytes.

HTTP method
-----------

In both Python 2 and 3 this should be a `str` object, that only contains bytes
from the ASCII range. Note that in Python 2 this represents a binary string and
in Python 3 it means Unicode text. Since the HTTP method name can only include
ASCII characters, the distinction is not important and using `str` makes it
easy to write code that's compatible with both Python 2 and 3.

URL
---

Same as the HTTP method, it should be a string that only uses ASCII
characters. Note that this means that libsaas methods should take care to
encode user input adecuately before handing the :class:`Request` over to the
executor and they need to be prepared to accept both byte strings and text.

Query parameters
----------------

This can either be a mapping of strings to strings or a simple string
value. The executor will accept both byte strings and text for keys and values
of the mapping, as well as numbers. It is the executor's responsibility to
correctly encode and quote those value before making a HTTP request to the
server.

HTTP headers
------------

This should be a mapping of strings using ASCII characters to ASCII characters
only (just like the HTTP method or the URL). According to RFC 2616 non-ASCII
characters are allowed in headers, but should be mime-encoded (as defined in
RFC 20147). If you need to use such values, encode them before handing the
:class:`Request` over to the executor.

Parsers
~~~~~~~

Data passed to parsers from the executor is always binary, which means that on
Python 2 it will be a `str` and on Python 3 it will be `bytes`. It is the
parser's responsibility to deal with any encoding issues.
