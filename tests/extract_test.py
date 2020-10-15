'''Test extract module.

Tests 1 function:
- output_raw_transactions
'''

import csv
from io import StringIO

from extract.read_from_s3 import output_raw_transactions

def test_output_raw_transactions():
    '''Test `output_raw_transactions` returns list of transaction dictionaries.
    '''
    # ARRANGE
    # Create example csv file for function to read
    example_row_string = '29/09/2020 09:00,Isle of Wight,Paul Kifer,"Regular Luxury hot chocolate - 2.40, Regular Flavoured hot chocolate - Hazelnut - £2.60",5.00,CASH,'
    example_row_bytes = StringIO(example_row_string)
    example_csv = csv.reader(example_row_bytes)
    # Create expected class instance output
    expected_output = [{
        'date': '29/09/2020 09:00',
        'location': 'Isle of Wight',
        'customer_name': 'Paul Kifer',
        'basket': "Regular Luxury hot chocolate - 2.40, Regular Flavoured hot chocolate - Hazelnut - £2.60",
        'pay_amount': '5.00',
        'payment_method': 'CASH',
        'ccn': '',
        'id_number': 0
    }]
    # ACT
    actual_output = output_raw_transactions(example_csv, skip_header=False)
    # ASSERT
    assert len(actual_output) == len(expected_output)
    assert actual_output == expected_output
