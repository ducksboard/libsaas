import contextlib
import inspect
from functools import update_wrapper

from libsaas import http, parsers
from libsaas.executors import base, current

decorator = None
try:
    import decorator
except ImportError:
    pass


def wrap(wrapper, wrapped):
    """
    Either use the decorator module, or the builtin functools.update_wrapper
    function to wrap one function with another.

    Using decorator is preferred, because it maintains argument specification,
    making automatic documentation output look better.
    """
    if decorator:
        return decorator.decorator(wrapper, wrapped)
    return update_wrapper(wrapper, wrapped)


def serialize_param(val):
    if isinstance(val, bool):
        return 'true' if val else 'false'
    return val


def translate_identity(val):
    return val


def get_params(param_names, param_store, serialize_param=serialize_param,
               translate_param=translate_identity):
    """
    Return a dictionary suitable to be used as params in a libsaas.http.Request
    object.

    Arguments are a tuple of parameter names, a dictionary mapping those names
    to parameter values and an optional custom parameter serialization
    function. This is useful for constructs like

    def apifunc(self, p1, p2, p3=None):
        params = get_params(('p1', 'p2', 'p3'), locals())

    which will extract parameters from the called method's environment.

    As an additional convenience, if param_names is None, all parameters from
    the param store will be considered, except for 'self'. This allows for even
    shorter code in the common situation.

    The serialization function can be used for instance when the service
    expects boolean values to be represented as '0' and '1' instead of 'true'
    and 'false' or when it accepts types that can be mapped to Python types and
    mandates a specific way of encoding them as strings.

    The translation function allows changing the param name before serializing
    it. For instance, param names abused to provide inequalities, like
    'start_time<=' need such translation since 'start_time<' is not a valid
    variable name in Python. The function is expected to return the name
    to use as the query param in the URL.
    """
    if param_names is None:
        param_names = [name for name in param_store.keys() if name != 'self']

    return dict((translate_param(name), serialize_param(param_store[name]))
                for name in param_names if param_store.get(name) is not None)


class MethodNotSupported(NotImplementedError):
    """
    This resource does not implement the method.
    """
    def __str__(self):
        return self.__class__.__doc__


def apimethod(f):

    def wrapped(*args, **kwargs):
        # when using decorator the first argument passed to the wrapping
        # function is the wrapped function, so discard it if it's the case
        if args and args[0] is f:
            args = args[1:]

        # call the wrapped function, apply the filters and pass the result on
        # to the executor
        request, parser = f(*args, **kwargs)
        args[0].apply_filters(request)
        return current.process(request, parser)

    wrapped = wrap(wrapped, f)
    wrapped.is_apimethod = True
    return wrapped


def resource(*klasses):

    def wrapper(f):
        f.is_resource = True
        f.produces = klasses
        return f

    return wrapper


@contextlib.contextmanager
def extract_request():
    """
    A context manager that helps extracting the Request object from a function
    decorated with the apimethod decorator.

    Usage is:

       with extract_request():
           request = self.decorated_method()

    It works by temporarily substituting the executor with a dummy one that
    just returns the request unchanged.
    """
    prev = base.current_executor()
    try:
        base.use_executor(lambda request, _: request)
        yield
    finally:
        base.use_executor(prev)


@contextlib.contextmanager
def change_parser(parser):
    """
    A context manager that allows overriding the function that will be used to
    parse the response.

    Usage is

       with change_parser(new_parser):
           result = service.resource().method()

    It works by temporarily substituting the executor with one that replaces
    the provided parser function with the one the context manager received.
    """
    prev = base.current_executor()
    try:
        base.use_executor(lambda request, _: prev(request, parser))
        yield
    finally:
        base.use_executor(prev)


def methods_with_attribute(cls, attribute):
    return [name for name, method in
            inspect.getmembers(cls, (lambda obj: inspect.isroutine(obj) and
                                     getattr(obj, attribute, False)))]


class Resource(object):
    """
    Base class for all resources.
    """
    filters = ()
    parent = None

    @classmethod
    def list_resources(cls):
        return methods_with_attribute(cls, 'is_resource')

    @classmethod
    def list_methods(cls):
        return methods_with_attribute(cls, 'is_apimethod')

    def __init__(self, parent):
        self.parent = parent

    def require(self, condition):
        if not condition:
            raise MethodNotSupported()

    def add_filter(self, filter_function):
        self.filters += (filter_function, )

    def apply_filters(self, request):
        if self.parent is not None:
            self.parent.apply_filters(request)

        for f in self.filters:
            f(request)


class HierarchicalResource(Resource):
    """
    Base class for resources whose URL is relative to a parent resource's URL.
    """
    path = None

    def __init__(self, parent, object_id=None):
        self.parent = parent
        self.object_id = object_id

        if self.object_id:
            self.object_id = http.quote_any(self.object_id)

    def get_url(self):
        if self.object_id is None:
            return '{0}/{1}'.format(self.parent.get_url(), self.path)

        return '{0}/{1}/{2}'.format(self.parent.get_url(), self.path,
                                    self.object_id)


class RESTResource(HierarchicalResource):
    """
    Base class for resources implementing the classical CRUD operations with
    HTTP verbs.
    """
    @apimethod
    def get(self):
        """
        For single-object resources, fetch the object's data. For collections,
        fetch all of the objects.
        """
        request = http.Request('GET', self.get_url())

        return request, parsers.parse_json

    @apimethod
    def create(self, obj):
        """
        Create a new resource.

        :var obj: a Python object representing the resource to be created,
            usually in the same format as returned from `get`. Refer to the
            upstream documentation for details.
        """
        self.require_collection()
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json

    @apimethod
    def update(self, obj):
        """
        Update this resource.

        :var obj: a Python object representing the updated resource, usually in
            the same format as returned from `get`. Refer to the upstream
            documentation for details.
        """
        self.require_item()
        request = http.Request('PUT', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json

    @apimethod
    def delete(self):
        """
        Delete this resource.
        """
        self.require_item()
        request = http.Request('DELETE', self.get_url())

        return request, parsers.parse_empty

    def require_collection(self):
        if self.object_id is not None:
            raise MethodNotSupported()

    def require_item(self):
        if self.object_id is None:
            raise MethodNotSupported()

    def wrap_object(self, obj):
        return obj
