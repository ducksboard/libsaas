#!/usr/bin/env python
"""
This script generates documentation files that get used when building the
libsaas API documentation.

It crawls docstrings from modules in the libsaas.services package.
"""
import inspect
import os
import pkgutil
import sys

sys.path.insert(0, os.path.abspath('..'))

from libsaas import services
from libsaas.services import base


def _title(title, char):
    return '\n{0}\n{1}\n\n'.format(title, char * len(title))


def method_path(resource, method):
    return '.'.join((resource.__module__,
                     resource.__name__,
                     method.__name__))


def walk_resource(resource, rst, top):
    for child_name in resource.list_resources():
        method = getattr(resource, child_name)
        path = method_path(resource, method)
        section_name = ', '.join([p.__name__ for p in method.produces])
        rst.write(_title(section_name, '-'))
        rst.write('.. automethod:: {0}\n'.format(path))

        for child_resource in method.produces:
            walk_resource(child_resource, rst, False)

    methods = resource.list_methods()
    if not methods:
        return

    if top:
        rst.write(_title('Service methods', '-'))

    for child_name in methods:
        method = getattr(resource, child_name)
        path = method_path(resource, method)
        rst.write('.. automethod:: {0}\n'.format(path))


def is_resource(klass):
    return inspect.isclass(klass) and issubclass(klass, base.Resource)


def process_package(importer, modname):
    module = importer.find_module(modname).load_module(modname)
    klass = inspect.getmembers(module, is_resource)[0][1]

    rst = open(os.path.join('generated', '{0}.rst'.format(modname)), 'w')

    rst.write(_title(klass.__name__, '='))
    rst.write('.. autoclass:: {0}.{1}\n'.format(modname, klass.__name__))

    walk_resource(klass, rst, True)

    rst.close()


def generate_index(modules):
    rst = open(os.path.join('generated', 'services.rst'), 'w')

    rst.write(_title('Supported services', '='))
    rst.write('.. toctree::\n    :maxdepth: 1\n\n')
    for importer, modname, is_package in modules:
        if not is_package:
            continue
        rst.write('    {0}\n'.format(modname))

    rst.close()


modules = sorted(pkgutil.iter_modules(services.__path__),
                 key=lambda tup: tup[1])

for importer, modname, is_package in modules:
    if not is_package:
        continue

    process_package(importer, modname)

generate_index(modules)
