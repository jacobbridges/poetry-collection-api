"""
api.py

Programmatic access to the poetry collection.
"""


class UnderConstructionError(BaseException):
    message = 'This feature is still under heavy development. Thank you for your patience.'
    pass


class ResourceFieldError(BaseException):
    message = 'Field "{field}" does not exist on {resource}'

    def __init__(self, field, resource):
        self.message = self.message.format(field=field, resource=resource.__class__.__name__)
        super(ResourceFieldError, self).__init__(self.message)


class PoetryApi(object):
    pass


class Resource(object):
    """
    Base for resources to extend.
    """
    def __init__(self, fields):
        self.fields = fields
        self._data = dict(zip(fields, ([None] * len(fields))))

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        if key in self.fields:
            self._data[key] = value
        else:
            raise ResourceFieldError(key, self)


class Collection(object):
    """
    Base for collections to extend.
    """
    def __init__(self):
        self.resources = []
        self._length = 0

    @property
    def length(self):
        return self._length
    count = length

    def paginate(self, limit=10, offset=0):
        raise UnderConstructionError

    def filter(self, pattern=None):
        raise UnderConstructionError

    def sort(self, *keys):
        raise UnderConstructionError


class Poem(Resource):
    """
    Represents a poem resource.
    """
    def __init__(self):
        super(Poem, self).__init__(['title', 'author', 'text', 'keywords', 'year', 'reference', 'period',
                                    'classification', 'region'])
