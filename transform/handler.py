'''UNFINISHED!!! Clean data from SQS and send to SQS

1. Receive a JSON list of raw transactions from SQS
2. Convert to a list of clean transactions and a list of baskets
'''
import json, os

import boto3

from transform import clean_transactions, create_baskets

def start(event, context):
    print ("Transform lambda start")
    
    # TODO Connect to SQS
    print('Connect to ')
    sqs = boto3.resource('sqs')
    print('Connected to SQS')
    queue = sqs.get_queue_by_name(QueueName='PUT NAME HERE')

    # TODO Read raw_transactions data from SQS json
    for message in queue.receive_messages():
        raw_transactions = 'SOMETHING!'
    print('Read JSON data')

    # Clean data
    clean_transaction_list = clean_transactions(raw_transactions)
    print('Cleaned transactions')
    basket_list = create_baskets(clean_transaction_list)
    print('Created baskets')

    # Output json data to SQS
    json_data = json.dumps({
        'transactions': clean_transaction_list,
        'baskets': basket_list
    })
