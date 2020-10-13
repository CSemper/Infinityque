import os
import sys
import boto3
from read_from_s3 import get_file_name, read_csv_file_from_s3, output_raw_transactions
from raw_class import Raw_Transaction

def start(event, context):
    try: 
        file_name = get_file_name()
    except Exception as ERROR:
        print ("Couldn't extract from S3 files")
        print (str(ERROR))
    
    try:
        data = read_csv_file_from_s3(bucket="group3-testbucket", key=file_name)
        print('Read data from csv')
        raw_transactions = output_raw_transactions(data)
        transactions_dict = {}
        for transaction in raw_transactions:
            transactions_dict.setdefault(transaction.id_number, []).append(transaction)
        for key, value in transactions_dict.items():
            print(key, ' : ', value)
        print('Read raw transactions')
    except Exception as ERROR:
        print ("Couldn't extract from S3 files")
        print (str(ERROR))
