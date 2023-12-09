import functools
import itertools
import math
import operator
import reprlib
from array import array


class Vector:
    typecode = 'd'
    __match_args__ = ('x', 'y', 'z', 't')

    def __init__(self, components):
        self._components = components

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):]
        return f'Vector({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.hypot(*self)

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        index = operator.index(key)
        return self._components[index]

    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1

        if 0 <= pos < len(self._components):
            return self._components[pos]
        msg = f'{cls.__name__!r} object has no attribute {name!r}'
        raise AttributeError(msg)

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.__match_args__:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attrubutes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''

            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)

    def angle(self, n):
        r = math.hypot(*self[n:])
        a = math.atan2(r, self[n - 1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - 1
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'

        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(', '.join(components))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)


if __name__ == '__main__':
    # A ``Vector`` is built from an iterable of numbers:
    v = Vector([1, 2, 3, 4] * 10)

    assert repr(v) == 'Vector([1, 2, 3, 4, 1, 2, ...])'
    assert bytes(Vector([1, 2, 3, 4])) == b'd\x01\x02\x03\x04'
    first, second = Vector([1, 2])
    assert first == 1 and second == 2
    assert bool(v)
    assert abs(Vector([3, 4])) == 5.0
    assert v == [1, 2, 3, 4] * 10

    # Test of slicing
    assert v[1] == 2
    assert type(v[1]) == int
    assert v[1:4] == (2, 3, 4)
    assert type(v[1:3]) == Vector
    v7 = Vector(range(7))
    assert v7[-1] == 6.0
    assert v7[1:4] == Vector([1.0, 2.0, 3.0])
    assert v7[-1:] == Vector([6.0])
    try:
        assert v7[1, 2]
    except TypeError as e:
        assert str(e) == "'tuple' object cannot be interpreted as an integer"

    # Tests of dynamic attribute access
    assert (v.x, v.y, v.z, v.t) == (v[0], v[1], v[2], v[3])
    try:
        v.x = 1
    except AttributeError as e:
        assert str(e) == "readonly attribute 'x'"
    try:
        v.f = 1
    except AttributeError as e:
        assert str(e) == "can't set attrubutes 'a' to 'z' in 'Vector'"
    try:
        v.f
    except AttributeError as e:
        assert str(e) == "'Vector' object has no attribute 'f'"

    # Tests of hashing:
    v1 = Vector([3, 4])
    v2 = Vector([3.1, 4.2])
    v3 = Vector([3, 4, 5])
    v6 = Vector(range(6))
    assert (hash(v1), hash(v3), hash(v6)) == (7, 2, 1)

    # Tests of ``format()``
    assert format(Vector([-1, -1, -1, -1]), 'h') == '<2.0, 2.0943951023931957, 2.186276035465284, 5.283185307179586>'
    assert format(Vector([2, 2, 2, 2]), '.3eh') == '<4.000e+00, 1.047e+00, 9.553e-01, 7.854e-01>'
    assert format(Vector([0, 1, 0, 0]), '0.5fh') == '<1.00000, 1.57080, 0.00000, 0.00000>'
