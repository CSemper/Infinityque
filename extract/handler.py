import json
import os
import sys

import boto3

from read_from_s3 import (get_file_names, get_key_suffix,
                          output_raw_transactions, read_csv_file_from_s3)
from sqs_messaging import send_message_list_to_sqs, split_long_list

def start(event, context):
    try:
        all_files = get_file_names()
    except Exception as ERROR:
        print('ERROR: Failed to connect to S3')
        print(str(ERROR))
    for file_name in all_files:
        print('EXTRACT START')
        print(file_name)
        try:
            # Read data
            data = read_csv_file_from_s3(bucket="cafe-transactions", key=file_name)
        except Exception as ERROR:
            print("ERROR: Couldn't read csv")
            print(str(ERROR))
            continue
        print('SUCCESS: Read data from csv')
        identifier = get_key_suffix(file_name)
        raw_transactions = output_raw_transactions(data, identifier)
        print('Read raw transactions')
        # Split data into smaller chunks to send on SQS
        raw_transaction_chunks = split_long_list(raw_transactions, max_length=750)
        print(f'Split into {len(raw_transaction_chunks)} chunk(s)')
        message_list = [json.dumps(chunk) for chunk in raw_transaction_chunks]
        print('Converted to JSON')
        
        # Send each json data chunk to SQS
        queue_name = 'Group3SQSExtracttoTransform'
        queue_url = 'https://sqs.eu-west-1.amazonaws.com/579154747729/Group3SQSExtracttoTransform'
        send_message_list_to_sqs(message_list, queue_name, queue_url)            
