import csv
import datetime

import boto3

from raw_class import Raw_Transaction

def get_key_prefix():
     today = datetime.date.today()
     yesterday = today - datetime.timedelta(days=1)
     key_prefix = yesterday.strftime("%Y/%m/%d") 
     return(key_prefix) 
 
def get_file_name():
    '''Returns csv file name for a given location and date.'''
    # List all files in bucket
    s3 = boto3.resource('s3')
    bucket = s3.Bucket("group3-testbucket")
    all_files = (file.key for file in bucket.objects.all())
    file_name_start = get_key_prefix()
    for file_name in all_files:
        if file_name.startswith(file_name_start):
            return file_name


def read_csv_file_from_s3(bucket, key):
    s3 = boto3.client('s3')
    s3_object = s3.get_object(Bucket=bucket,
                              Key=key)
    data = s3_object['Body'].read().decode('utf-8')
    return csv.reader(data.splitlines())

def output_raw_transactions(csv_reader, skip_header=True):
    raw_transaction_list = []
    if skip_header:
        next(csv_reader)
    counter = 0
    for line in csv_reader:
        try:
            identity = counter
            raw_transaction = Raw_Transaction(line[0], line[1], line[2], line[3], line[4], line[5], line[6], identity)
            raw_transaction_list.append(raw_transaction)
            counter = counter + 1
        except ValueError:
            print('Failed to read row:')
            print(line)
            continue
    return raw_transaction_list
