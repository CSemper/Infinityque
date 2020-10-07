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

def create_sql_transactions_string(list_transactions, table='transactions_g3'):
    '''Converts list of transactions to SQL insert query string.
    '''
    def create_one_row(transaction_instance):
        return f'''VALUES(
    '{transaction_instance.unique_id}',
    '{transaction_instance.date}',
    '{transaction_instance.first_name}',
    {transaction_instance.total},
    '{transaction_instance.location}'
)'''
    # ----------
    values_to_insert = []
    for transaction in list_transactions:
        values_to_insert.append(create_one_row(transaction))
    values_string = f'''
INSERT INTO {table} (
    unique_id,
    date,
    first_name,
    total,
    location
)
'''
    values_string += ',\n'.join(values_to_insert)
    return values_string + ';'

def create_sql_basket_string(list_baskets, table='basket_g3'):
    '''Converts list of baskets to SQL insert query string.
    '''
    "INSERT INTO basket (transaction_id, item, cost) VALUES (%s, %s, %s)"
    def create_one_row(basket_instance):
        return f'''VALUES(
    '{basket_instance.trans_id}',
    '{basket_instance.item}',
    {basket_instance.cost}
)'''
    # ----------
    values_to_insert = []
    for transaction in list_baskets:
        values_to_insert.append(create_one_row(transaction))
    values_string = f'''
INSERT INTO {table} (
    transaction_id,
    item,
    cost
)
'''
    values_string += ',\n'.join(values_to_insert)
    return values_string + ';'