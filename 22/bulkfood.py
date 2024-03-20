import pytest

def quantity(storage_name):
    def qty_getter(instance):
        return instance.__dict__[storage_name]

    def qty_setter(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)


class LineItem:
    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


def test_line_items_properties():
    product = LineItem('Product', 8, 13.95)
    assert (product.weight, product.price) == (8, 13.95)

    with pytest.raises(ValueError) as exc:
        product.weight = -1

    assert 'value must be > 0' == str(exc.value)

    with pytest.raises(ValueError) as exc:
        LineItem('Product', 1, -2)

    assert 'value must be > 0' == str(exc.value)



