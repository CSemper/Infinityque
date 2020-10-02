'''Test data_handling functions.'''
from csv import reader
from io import StringIO

import pytest

from src.classes import RawTransaction, Basket
from src.data_handling import to_raw_transactions, split_basket

def test_to_raw_transactions():
    '''Test `to_raw_transactions` function returns class with correct attributes.
    '''
    # Create example csv file for `to_raw_transactions` to read
    example_row_string = '29/09/2020 09:00,Isle of Wight,Paul Kifer,"Regular Luxury hot chocolate - £2.40, Regular Flavoured hot chocolate - Hazelnut - £2.60",5.00,CASH,'
    example_row_bytes = StringIO(example_row_string)
    example_csv = reader(example_row_bytes)
    # Create expected class instance output
    expected_output = RawTransaction(
        date = '29/09/2020 09:00',
        location = 'Isle of Wight',
        customer_name = 'Paul Kifer',
        basket = "Regular Luxury hot chocolate - £2.40, Regular Flavoured hot chocolate - Hazelnut - £2.60",
        pay_amount = '5.00',
        payment_method = 'CASH',
        ccn = ''
    )
    # Act
    actual_output = next(to_raw_transactions(example_csv, skip_header=False))
    # Assert
    assert actual_output.date == expected_output.date
    assert actual_output.location == expected_output.location
    assert actual_output.customer_name == expected_output.customer_name
    assert actual_output.basket == expected_output.basket
    assert actual_output.pay_amount == expected_output.pay_amount
    assert actual_output.payment_method == expected_output.payment_method
    assert actual_output.ccn == expected_output.ccn

def test_split_basket():
    # Arrange
    example_basket = "Regular Luxury hot chocolate - £2.40, Regular Flavoured hot chocolate - Hazelnut - £2.60"
    expected_output = [
        Basket(item='Regular Luxury hot chocolate',
               cost='£2.40'),
        Basket(item='Regular Flavoured hot chocolate - Hazelnut',
               cost='£2.60')
    ]
    # Act
    actual_output = list(split_basket(example_basket))
    # Assert
    assert len(expected_output) == len(actual_output)

    for actual_basket, expected_basket in zip(actual_output, expected_output):
        assert actual_basket.item == expected_basket.item
        assert actual_basket.cost == expected_basket.cost
