import os
import sys
import boto3
import json
from read_from_s3 import get_file_names, read_csv_file_from_s3, output_raw_transactions
from raw_class import Raw_Transaction

def start(event, context):
    try:
        all_files = get_file_names()
    except Exception as ERROR:
        print ("Couldn't extract from S3 files")
        print (str(ERROR))
    for file_name in all_files:
        try:
            # Read data
            data = read_csv_file_from_s3(bucket="group3-testbucket", key=file_name)
            print('Read data from csv')
            raw_transactions = output_raw_transactions(data)
            print('Read raw transactions')
            json_data = json.dumps(raw_transactions)
            print('Converted to JSON')
        except Exception as ERROR:
            print ("Couldn't extract from S3 files")
            print (str(ERROR))
        # Send JSON in SQS
        
