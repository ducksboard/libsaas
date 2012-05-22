from . import base

__all__ = ['TestExecutor']


class TestExecutor(object):
    """
    An executor that just stores the request and passes a pre-set response to
    the parser.
    """
    def set_response(self, content, code, headers):
        self.content = content
        self.code = code
        self.headers = headers

    def __call__(self, request, parser):
        self.request = request
        return parser(self.content, self.code, self.headers)


def use():
    executor = TestExecutor()
    base.use_executor(executor)
    return executor
