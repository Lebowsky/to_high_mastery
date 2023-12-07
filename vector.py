import math
import reprlib
from array import array


class Vector:
    typecode = 'd'

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

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)


if __name__ == '__main__':
    v = Vector([1, 2, 3, 4]*10)
    print(v)
    print(repr(v))
    print(bytes(v))
    print(Vector.frombytes(bytes(v)))
    print(*v)
    print(bool(v))
    print(abs(v))
    print(v == [1, 2, 3, 4]*10)
