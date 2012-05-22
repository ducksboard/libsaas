import logging
import requests

from libsaas import http
from . import base

__all__ = ['requests_executor']


logger = logging.getLogger('libsaas.executor.requests_executor')


extra_params = {'extra': {}}


def requests_executor(request, parser):
    """
    An executor using the requests module.
    """
    logger.info('requesting %r', request)

    logger.debug('request uri: %r, data: %r, headers: %r',
                 request.uri, request.params, request.headers)

    kwargs = {'method': request.method, 'url': request.uri,
              'headers': request.headers}
    kwargs.update(extra_params['extra'])

    if request.params:
        if request.method.upper() in http.URLENCODE_METHODS:
            kwargs['params'] = request.params
        else:
            kwargs['data'] = request.params

    resp = requests.request(**kwargs)

    logger.debug('response code: %r, body: %r, headers: %r',
                 resp.status_code, resp.content, resp.headers)

    return parser(resp.content, resp.status_code, resp.headers)


def use(**extra):
    base.use_executor(requests_executor)
    extra_params['extra'] = extra
