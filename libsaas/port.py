"""
Utilities for writing code compatible with different versions of Python.

Mostly stolen from six, but we don't want to make it a dependency.
"""
import sys


PY3 = sys.version_info[0] == 3

if PY3:
    text_type = str
    binary_type = bytes
else:
    text_type = unicode
    binary_type = str


def to_u(val, encoding='utf-8'):
    """
    Take a text (unicode) or binary value and return unicode. Binary values are
    decoded using the provided encoding.
    """
    if isinstance(val, text_type):
        return val

    return val.decode(encoding)
