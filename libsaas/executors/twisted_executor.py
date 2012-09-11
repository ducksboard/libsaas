import logging

from twisted.internet import defer, protocol, reactor
from twisted.web import client, http, http_headers
from twisted.web.iweb import IBodyProducer
from zope.interface import implements

from libsaas import port
from libsaas import http as our_http

from . import base

__all__ = ['TwistedExecutor']


logger = logging.getLogger('libsaas.executor.twisted_executor')


class StringBodyProducer(object):
    """
    A IBodyProducer that just writes the passed string as-is.
    """
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(self.body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return defer.succeed(None)

    def stopProducing(self):
        pass

    def pauseProducing(self):
        pass

    def resumeProducing(self):
        pass


class HTTPResponseProtocol(protocol.Protocol):
    """
    A simple protocol class to interpret data from a Twisted response.
    """
    def __init__(self, parser, tolerant=False):
        self.parser = parser
        self.buffer = port.StringIO()
        self.ok_reasons = [client.ResponseDone]
        if tolerant:
            self.ok_reasons.append(http.PotentialDataLoss)

    def handle_response(self, response):
        self.finished = defer.Deferred(self.cancel)
        self.code = response.code
        self.phrase = response.phrase
        self.headers = response.headers

        response.deliverBody(self)
        return self.finished

    def dataReceived(self, data):
        self.buffer.write(data)

    def connectionLost(self, reason):
        if not self.finished:
            return

        if not reason.check(*self.ok_reasons):
            self.finished.errback(reason)
            return

        try:
            headers = dict((k.lower(), v[0])
                           for k, v in self.headers.getAllRawHeaders())
            ret = self.parser(self.buffer.getvalue(), self.code, headers)
        except:
            self.finished.errback()
        else:
            self.finished.callback(ret)

    def cancel(self, d):
        self.finished = None
        self.stopProducing()


class TwistedExecutor(object):
    """
    An executor using Twisted's Agent. It returns Deferreds that fire with the
    parsed output.
    """
    agent = client.Agent(reactor)

    def __init__(self, agent, tolerant):
        if agent is not None:
            self.agent = agent
        self.tolerant = tolerant

    def __call__(self, request, parser):
        logger.info('requesting %r', request)

        uri = request.uri
        producer = None

        if request.method.upper() in our_http.URLENCODE_METHODS:
            uri = self.encode_uri(request)
        else:
            producer = self.body_producer(request.params)
            content_type = 'application/x-www-form-urlencoded'
            request.headers['Content-Type'] = content_type

        logger.debug('request uri: %r, producer: %r, headers: %r',
                     uri, producer, request.headers)

        headers = self.prepare_headers(request.headers)

        d = self.agent.request(method=request.method, uri=uri,
                               headers=headers, bodyProducer=producer)
        return d.addCallback(self.got_response, parser)

    def encode_uri(self, request):
        if not request.params:
            return request.uri

        return request.uri + '?' + our_http.urlencode_any(request.params)

    def body_producer(self, params):
        if not params:
            return None

        payload = params
        if isinstance(params, dict):
            payload = our_http.urlencode_any(params)

        return StringBodyProducer(payload)

    def prepare_headers(self, headers):
        prepared = dict((name, [val]) for name, val in headers.items())
        return http_headers.Headers(prepared)

    def got_response(self, response, parser):
        """
        Handle a Twisted HTTP Response. Read and interpret the entire response
        body and report the result. Returns a Deferred that will fire with the
        content, possible processed in some way, or errback if there has been
        an error reading the response or if the response itself is errorneous.
        """
        protocol = HTTPResponseProtocol(parser, self.tolerant)
        return protocol.handle_response(response)


def use(agent=None, tolerant=False):
    base.use_executor(TwistedExecutor(agent, tolerant))
