import operator
from .core import _BaseField

identity = lambda x: x


def makemethod(function):
    """Returns a method that returns the given function applied to the value of
    the field"""
    def magicmethod(self, *args, **kwargs):
        return MagicField(lambda s: function(*args, **kwargs)(self._compute(s)))
    return magicmethod


class MagicField(_BaseField):
    def __init__(self, constructor=identity):
        self.constructor = constructor

    def _compute(self, soup):
        return self.constructor(soup)

    __getattr__ = makemethod(operator.attrgetter)
    __getitem__ = makemethod(operator.itemgetter)

    def __call__(self, *args, **kwargs):
        return MagicField(lambda s: self._compute(s)(*args, **kwargs))

    # TODO : any magic method can be defined here
