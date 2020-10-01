'''Provides functions to read data from S3 buckets and convert to classes.
'''
import boto3
import csv

from classes import RawTransaction, Transaction, Basket

def find_last_csv_name(bucket):
    '''Finds last file-name in S3 bucket when sorted alphabetically.'''
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    files = (file.key for file in bucket.objects.all())
    return min(files)

def read_s3_csv(bucket, key):
    '''Return csv.reader object from S3 csv.'''
    s3 = boto3.client('s3')
    s3_object = s3.get_object(Bucket=bucket,
                              Key=key)
    data = s3_object['Body'].read().decode('utf-8')
    return csv.reader(data.splitlines())

def to_raw_transactions(csv_reader, skip_header=True):
    '''Converts each row of a csv.reader object to a RawTransaction object.'''
    # Don't read first row if it's a header
    if skip_header:
        next(csv_reader)
    for row in csv_reader:
        try:
            yield RawTransaction(*row)
        except ValueError:
            print('Failed to read row:')
            print(row)
            continue

def to_clean_transactions(raw_transactions):
    '''Converts each RawTransaction object in list to a Transaction object.'''
    for raw_transaction in raw_transactions:
        clean_transaction = Transaction(
            location=raw_transaction.location,
            customer=raw_transaction.customer_name,
            datetime=raw_transaction.date,
            total=float(raw_transaction.pay_amount)
        )
        yield clean_transaction

def split_basket(basket):
    '''Converts each (item, cost) pair in a string to a Basket object.'''
    baskets = []
    for sale in basket.split(', '):
        item, cost = sale.split(' - ')
        baskets.append(Basket(item=item, cost=cost))
    return baskets
