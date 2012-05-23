"""
Implementation for the saas script distributed with libsaas.
"""
import collections
import inspect
import json
import logging
import optparse
import pprint
from itertools import chain, repeat

from libsaas.services import base


def extract_action(instance, parser, args):
    resource = instance

    # consume arguments until reaching an apimethod
    while args:
        current = args[0]
        resource = getattr(resource, current, None)

        if not resource:
            parser.error('no such resource %s' % args[0])
        if getattr(resource, 'is_apimethod', False):
            return resource, args[1:]
        if not isinstance(resource, collections.Callable):
            parser.error('no such resource %s' % args[0])

        # consume one token
        args.pop(0)

        # find out how many arguments does our callable take
        argspec = inspect.getargspec(resource)

        # consume as many tokens
        to_consume = len(argspec.args) - 1
        if len(args) < to_consume:
            msg = '{0} needs {1} params, {2} given'
            parser.error(msg.format(current, to_consume, len(args)))

        # produce a new resource by passing the consumed arguments to the
        # resource
        consumed, args = args[:to_consume], args[to_consume:]
        resource = resource(*list(map(try_interpret_arg, consumed)))

    parser.error('not enough arguments')


def try_interpret_arg(arg):
    try:
        return json.loads(arg)
    except:
        return arg


def parse_args(args):
    usage = ('usage: %prog service [service params] [general params] '
             '[resource|param, ...] method [param, ...]')
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('--verbose', '-v', dest='verbose',
                      action='count', default=0)
    parser.add_option('--executor', '-x', dest='executor', action='store')

    if len(args) < 2:
        parser.error('not enough arguments')

    service = args[1]

    # hack to detect if the first argument is -h or --help, since we don't call
    # parse_args before adding the service-specific parameters
    if service in ('-h', '--help'):
        parser.print_help()
        parser.exit()

    try:
        module = __import__('libsaas.services', globals(), locals(), [service])
        module = getattr(module, service)
    except (ImportError, AttributeError):
        parser.error('no such service %s' % service)

    members = inspect.getmembers(module, lambda obj: inspect.isclass(obj) and
                                 issubclass(obj, base.Resource))
    if not members:
        parser.error('no such service %s' % service)

    _, klass = members[0]

    # got the service class, inspect its __init__ method to extract the keyword
    # arguments
    argspec = inspect.getargspec(klass.__init__)
    for argname, default in zip(reversed(argspec.args),
                                 chain(reversed(argspec.defaults or ()),
                                       repeat(None))):
        if argname == 'self':
            continue
        optargs = {'dest': argname}
        if default is not None:
            optargs.update({'default': default})
        parser.add_option('--%s' % argname, **optargs)

    options, args = parser.parse_args(args)

    if options.executor:
        try:
            module_name = '{0}_executor'.format(options.executor)
            module = __import__('libsaas.executors', globals(), locals(),
                                [module_name])
            module = getattr(module, module_name)
        except ImportError:
            parser.error('no such executor %s' % options.executor)

        module.use()

    level = logging.ERROR
    if options.verbose > 1:
        level = logging.DEBUG
    elif options.verbose > 0:
        level = logging.INFO

    logging.basicConfig(level=level)

    del options.verbose
    del options.executor

    if len(args) < 2:
        parser.error('not enough arguments')

    # instantiate the class, get the resource
    instance = klass(**options.__dict__)
    action, args = extract_action(instance, parser, args[2:])
    pprint.pprint(action(*list(map(try_interpret_arg, args))))


def run(args):
    parse_args(args)
