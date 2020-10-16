import os
import sys
import boto3
import json
from read_from_s3 import get_file_names, read_csv_file_from_s3, output_raw_transactions, get_key_suffix
from send_dict_to_sqs import send_dict_to_sqs 

def start(event, context):
    try:
        all_files = get_file_names()
    except Exception as ERROR:
        print ("Couldn't extract from S3 files")
        print (str(ERROR))
    for file_name in all_files:
        try:
            # Read data
            data = read_csv_file_from_s3(bucket="cafe-transactions", key=file_name)
            print('Read data from csv')
            identifier = get_key_suffix(file_name)
            print(identifier)
            raw_transactions = output_raw_transactions(data, identifier)
            print('Read raw transactions')
            json_data = json.dumps(raw_transactions)
            print('Converted to JSON')
        except Exception as ERROR:
            print ("Couldn't extract from S3 files")
            print (str(ERROR))
          
        try:
          send_dict_to_sqs(json_data)
          print(f"{file_name} : data was sent to SQS")
        except Exception as ERROR:
          print(f"{file_name} : data was not sent to SQS")
          print(str(ERROR))
            
