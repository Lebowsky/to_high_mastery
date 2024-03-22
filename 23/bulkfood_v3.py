import pytest


class Quantity:
    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            msg = f'{self.storage_name} must be > 0'
            raise ValueError(msg)

    def __get__(self, instance, owner):
        return instance.__dict__[self.storage_name]


class LineItem:
    weight = Quantity('weight')
    price = Quantity('price')

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

    assert 'weight must be > 0' == str(exc.value)

    with pytest.raises(ValueError) as exc:
        LineItem('Product', 1, -2)

    assert 'price must be > 0' == str(exc.value)
