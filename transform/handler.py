
'''UNFINISHED!!! Clean data from SQS and send to SQS

1. Receive a JSON list of raw transactions from SQS
2. Convert to a list of clean transactions and a list of baskets
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
    json_data = json.dumps({
        'transactions': clean_transaction_list,
        'baskets': basket_list
    })
    try:
        send_dict_to_sqs(json_data)
        print('Sent data to SQS')
    except Exception as ERROR:
        print(str(ERROR))
        print('Failed to send data to SQS')
