import pytest

import model_v5 as model


class LineItem:
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

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
