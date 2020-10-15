'''Clean data from extract module and send to load module using SQS

1. Receive a JSON list of raw transactions from SQS
2. Convert to a list of clean transactions and a list of baskets
3. Send each list in an SQS message
'''
import json, os

import boto3
import json

from clean_data import clean_transactions, create_baskets
from send_dict_to_sqs import send_dict_to_sqs

def start(event, context):
    # Read message from SQS (list raw transactions)
    print ("Transform lambda start")
    raw_transactions_string = event['Records'][0]['body']
    raw_transactions = json.loads(raw_transactions_string)
    print('Read raw transactions data')

    # Clean data
    clean_transaction_list = clean_transactions(raw_transactions)
    print('Cleaned transactions')
    basket_list = create_baskets(clean_transaction_list)
    print('Created baskets')

    # Send json data to SQS
    transaction_data = json.dumps({
        'transactions': clean_transaction_list
    })
    basket_data = json.dumps({
        'baskets': basket_list
    })
    try:
        send_dict_to_sqs(transaction_data)
        print('Sent transaction data to SQS')
    except Exception as ERROR:
        print(str(ERROR))
        print('Failed to send transaction data to SQS')
    try:
        send_dict_to_sqs(basket_data)
        print('Sent basket data to SQS')
    except Exception as ERROR:
        print(str(ERROR))
        print('Failed to send basket data to SQS')
