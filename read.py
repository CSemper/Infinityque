import boto3
import csv
from classes import Raw_Transaction

raw_transaction_list = []

def return_most_recent_file(bucket):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    files = (file.key for file in bucket.objects.all())
    return min(files)

def read_csv_file_from_s3(bucket, key):
    s3 = boto3.client('s3')
    s3_object = s3.get_object(Bucket=bucket,
                              Key=key)
    data = s3_object['Body'].read().decode('utf-8')
    return csv.reader(data.splitlines())

def output_raw_transactions(csv_reader, skip_header=True):
    if skip_header:
        next(csv_reader)
    counter = 0
    for line in csv_reader:
        try:
            identity = counter + 1
            raw_transaction = Raw_Transaction(line[0], line[1], line[2], line[3], line[4], line[5], line[6], identity)
            raw_transaction_list.append(raw_transaction)
            counter+=1
        except ValueError:
            print('Failed to read row:')
            print(line)
            continue
    return raw_transaction_list
