import pytest

from gestor_de_stock.validators import is_valid_price


@pytest.mark.parametrize(
    "price, expected",
    [
        (10, True),
        (100, True),
        (1, True),
        (0, False),
        (-10, False),
    ],
)
def test_is_valid_price(price, expected):
    assert is_valid_price(price) is expected
