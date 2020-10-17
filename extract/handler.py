import json
import os
import sys

import boto3

from read_from_s3 import (get_file_names, get_key_suffix,
                          output_raw_transactions, read_csv_file_from_s3,
                          split_long_list)
from send_dict_to_sqs import send_dict_to_sqs

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
        raw_transaction_chunks = split_long_list(raw_transactions)
        print(f'Split into {len(raw_transaction_chunks)} chunk(s)')
        json_chunks = [json.dumps(chunk) for chunk in raw_transaction_chunks]
        print('Converted to JSON')
        
        # Send each json data chunk to SQS
        for count, json_chunk in enumerate(json_chunks, start=1):
            try:
                send_dict_to_sqs(json_chunk)
                print(f"SUCCESS: chunk {count}: data was sent to SQS")
            except Exception as ERROR:
                print(f"ERROR: chunk {count}: data was not sent to SQS")
                print(str(ERROR))
            
