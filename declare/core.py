from collections import OrderedDict


class _BaseField:
    """Base class for the various types of fields, acts as a common marker"""
    pass


class Field(_BaseField):
    """A basic field that takes a compuration function"""
    def __init__(self, constructor):
        self.constructor = constructor

    def _compute(self, soup):
        return self.constructor(soup)


class MapField(_BaseField):
    """A convenience field for a mapped list"""
    def __init__(self, function, constructor):
        self.function = function
        if hasattr(constructor, '_compute'):
            # constructor is actually a field
            self.constructor = constructor._compute
        else:
            self.constructor = constructor

    def _compute(self, soup):
        return [self.function(result) for result in self.constructor(soup)]


def prepare(f):
    """A decorator to mark functions as object preparation code"""
    f._is_prepare = True
    return f


class OrderedFieldsMetaClass(type):
    """A metaclass that registers the _BaseField attributes and the methods
    decorated with prepare and put heir names in cls._fields and
    cls._prepare (prepare contains both fields and methods)"""
    @classmethod
    def __prepare__(metacls, name, bases):
        return OrderedDict()

    def __new__(cls, name, bases, classdict):
        result = type.__new__(cls, name, bases, dict(classdict))
        result._fields = []
        result._prepare = []

        for attrname, attr in classdict.items():
            if isinstance(attr, _BaseField):
                result._fields.append(attrname)
                result._prepare.append(attrname)
            elif hasattr(attr, '_is_prepare'):
                result._prepare.append(attrname)
        return result


class Item(metaclass=OrderedFieldsMetaClass):
    """An item with declared fields. Fields and preparation methods are
    executed in the order of declaration, and fields are replaced with
    their value."""
    def __init__(self, soup):
        for attrname in self._prepare:
            attr = getattr(self, attrname)
            if isinstance(attr, _BaseField):
                # a field, replace with the computed value
                setattr(self, attrname, attr._compute(soup))
            else:
                # else, it's a prepare function
                attr(soup)

    def __repr__(self):
        values = ('{}={}'.format(field, repr(getattr(self, field)))
                  for field in self._fields)
        return '<{}: {}>'.format(type(self).__name__,
                                 ' '.join(values))
