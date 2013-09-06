from unittest import TestCase
from unittest.mock import Mock, MagicMock, sentinel


class FieldTest(TestCase):
    def test_basic_field(self):
        from declare import Field
        constructor = Mock(spec=[])
        field = Field(constructor)

        value = field._compute(sentinel.soup)

        constructor.assert_called_once_with(sentinel.soup)
        self.assertEqual(value, constructor())


class MapFieldTest(TestCase):
    def test_with_callable(self):
        from declare import MapField
        constructor = Mock(spec=[], return_value=[1, 2, 3])
        mapped_function = lambda x: x * 2
        field = MapField(mapped_function, constructor)

        value = field._compute(sentinel.soup)

        constructor.assert_called_once_with(sentinel.soup)
        self.assertEqual(value, [2, 4, 6])

    def test_with_field(self):
        from declare import Field, MapField
        constructor = Mock(spec=[], return_value=[1, 2, 3])
        argument_field = Field(constructor)
        mapped_function = lambda x: x * 2
        field = MapField(mapped_function, argument_field)

        value = field._compute(sentinel.soup)

        constructor.assert_called_once_with(sentinel.soup)
        self.assertEqual(value, [2, 4, 6])


class MagicFieldTest(TestCase):
    def test_empty(self):
        from declare import MAGIC

        value = MAGIC._compute(sentinel.soup)

        self.assertEqual(value, sentinel.soup)

    def test_getattr(self):
        from declare import MAGIC
        soup = Mock()
        field = MAGIC.someattribute

        value = field._compute(soup)

        self.assertEqual(value, soup.someattribute)

    def test_getitem(self):
        from declare import MAGIC
        soup = MagicMock()
        field = MAGIC['item']

        value = field._compute(soup)

        self.assertEqual(value, soup['item'])

    def test_call(self):
        from declare import MAGIC
        soup = Mock()
        field = MAGIC()

        value = field._compute(soup)

        self.assertEqual(value, soup())

    def test_complex(self):
        from declare import MAGIC
        soup = MagicMock()
        field = MAGIC.find('table')[2].get_text()

        value = field._compute(soup)

        self.assertEqual(value, soup.find('table')[2].get_text())


class OrderedFieldsMetaClassTest(TestCase):
    def test_one_field(self):
        from declare.core import _BaseField, OrderedFieldsMetaClass

        class Test(metaclass=OrderedFieldsMetaClass):
            f = _BaseField()
            g = 12

        self.assertEqual(Test._fields, ['f'])
        self.assertEqual(Test._prepare, ['f'])

    def test_one_prepare(self):
        from declare.core import prepare, OrderedFieldsMetaClass

        class Test(metaclass=OrderedFieldsMetaClass):
            @prepare
            def some_method():
                pass  # pragma: no cover

            def non_prepare_method():
                pass  # pragma: no cover

        self.assertEqual(Test._fields, [])
        self.assertEqual(Test._prepare, ['some_method'])

    def test_many_fields(self):
        from declare.core import _BaseField, OrderedFieldsMetaClass

        class Test(metaclass=OrderedFieldsMetaClass):
            pouet = _BaseField()
            truc = _BaseField()

        self.assertEqual(Test._fields, ['pouet', 'truc'])
        self.assertEqual(Test._prepare, ['pouet', 'truc'])

    def test_many_prepares(self):
        from declare.core import prepare, OrderedFieldsMetaClass

        class Test(metaclass=OrderedFieldsMetaClass):
            @prepare
            def some_method():
                pass  # pragma: no cover

            @prepare
            def some_other_method():
                pass  # pragma: no cover

        self.assertEqual(Test._fields, [])
        self.assertEqual(Test._prepare, ['some_method', 'some_other_method'])

    def test_many_prepares_and_fields(self):
        from declare.core import _BaseField, prepare, OrderedFieldsMetaClass

        class Test(metaclass=OrderedFieldsMetaClass):
            @prepare
            def some_method():
                pass  # pragma: no cover

            f = _BaseField()

            @prepare
            def some_other_method():
                pass  # pragma: no cover

        self.assertEqual(Test._fields, ['f'])
        self.assertEqual(Test._prepare, ['some_method', 'f',
                                         'some_other_method'])


class ItemTest(TestCase):
    def test_simple_field(self):
        from declare import Item, Field, MAGIC

        class Point(Item):
            x = Field(lambda s: s['x'])
            y = MAGIC['y']

        p = Point({'x': 12, 'y': 42})

        self.assertEqual(p.x, 12)
        self.assertEqual(p.y, 42)

    def test_simple_setup(self):
        from declare import Item, MAGIC, prepare

        class Point(Item):
            @prepare
            def prep(self, soup):
                # This is a complex multiline computation (yes it is)
                soup['x'] = soup['raw_x'] + 42

            x = MAGIC['x']

        p = Point({'raw_x': 12})

        self.assertEqual(p.x, 54)

    def test_complex_setup(self):
        from declare import Item, MAGIC, prepare

        class Blorg(Item):
            @prepare
            def prep1(self, soup):
                soup['bar'] = soup['foo'] + 1

            bar = MAGIC['bar']

            @prepare
            def prep2(self, soup):
                soup['baz'] = soup['bar'] + 2

            baz = MAGIC['baz']

        b = Blorg({'foo': 0})

        self.assertEqual(b.bar, 1)
        self.assertEqual(b.baz, 3)

    def test_repr(self):
        from declare import Item, MAGIC

        class Point(Item):
            x = MAGIC['x']
            y = MAGIC['y']

        p = Point({'x': 12, 'y': 42})

        self.assertEqual(repr(p),
                         '<Point: x=12 y=42>')
