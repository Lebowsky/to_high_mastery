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
        return tuple(self) == tuple(other)

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

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)


if __name__ == '__main__':
    v = Vector([1, 2, 3, 4] * 10)
    assert repr(v) == 'Vector([1, 2, 3, 4, 1, 2, ...])'
    assert bytes(Vector([1, 2, 3, 4])) == b'd\x01\x02\x03\x04'
    first, second = Vector([1, 2])
    assert first == 1 and second == 2
    assert bool(v)
    assert abs(Vector([3, 4])) == 5.0
    assert v == [1, 2, 3, 4] * 10
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

    print(Vector.frombytes(bytes(v)))
    # print(Vector.frombytes(b'd\x01\x02\x03\x04'))
