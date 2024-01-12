import pytest
from vector import Vector


def test_vector_can_built_from_an_iterable_of_numbers():
    """A ``Vector`` is built from an iterable of numbers:"""

    v = Vector([1, 2, 3, 4] * 10)

    assert repr(v) == 'Vector([1, 2, 3, 4, 1, 2, ...])'
    assert bytes(Vector([1, 2, 3, 4])) == b'd\x01\x02\x03\x04'
    first, second = Vector([1, 2])
    assert first == 1 and second == 2
    assert bool(v)
    assert abs(Vector([3, 4])) == 5.0
    assert v == [1, 2, 3, 4] * 10


def test_vector_can_use_slicing():
    """Test of slicing"""

    v = Vector([1, 2, 3, 4] * 10)

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


def test_vector_can_dynamic_attribute_access():
    """Tests of dynamic attribute access"""

    v = Vector([1, 2, 3, 4] * 10)

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


def test_vector_has_hashing():
    """ Tests of hashing: """

    v1 = Vector([3, 4])
    v2 = Vector([3.1, 4.2])
    v3 = Vector([3, 4, 5])
    v6 = Vector(range(6))
    assert (hash(v1), hash(v3), hash(v6)) == (7, 2, 1)


def test_vector_can_support_format_str():
    """Tests of ``format()``"""

    assert format(Vector([-1, -1, -1, -1]), 'h') == '<2.0, 2.0943951023931957, 2.186276035465284, 5.283185307179586>'
    assert format(Vector([2, 2, 2, 2]), '.3eh') == '<4.000e+00, 1.047e+00, 9.553e-01, 7.854e-01>'
    assert format(Vector([0, 1, 0, 0]), '0.5fh') == '<1.00000, 1.57080, 0.00000, 0.00000>'


def test_vector_can_concat():
    v1 = Vector([3, 4, 5])
    v2 = Vector([6, 7, 8])

    assert v1 + v2 == Vector([9, 11, 13])

    v1 = Vector([3, 4, 5, 6])
    v3 = Vector([1, 2])
    assert v1 + v3 == Vector([4, 6, 5, 6])

    v1 = Vector([3, 4, 5])
    assert (10, 20, 30) + v1 == Vector((13, 24, 35))

    v1 + 1


def test_vector_can_multiply_on_scalar():
    v = Vector([1, 2, 3])
    assert v * 10 == Vector([10, 20, 30])
    assert 11 * v == Vector([11, 22, 33])
    assert (v * True) == Vector([1, 2, 3])

    from fractions import Fraction
    assert v * Fraction(1, 3) == Vector([float(Fraction(1, 3) * 1), float(Fraction(1, 3)) * 2, 1.0])


def test_vector_support_scalar_multiply():
    va = Vector([1, 2, 3])
    vz = Vector([5, 6, 7])

    assert va @ vz == 38
    assert [10, 20, 30] @ vz == 380.0

    try:
        va @ 3
    except TypeError as e:
        assert type(e) is TypeError


if __name__ == '__main__':
    pass
