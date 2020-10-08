import os
import sys

import boto3
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

from read import get_file_name, output_raw_transactions, read_csv_file_from_s3
from transform import clean_basket_items, clean_transactions, update_raw_basket

load_dotenv()

def start(event, context):
    print ("This is the updated lambda")
    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT"))
    user = os.getenv("DB_USER")
    passwd = os.getenv("DB_PASS")
    db = os.getenv("DB_NAME")
    cluster = os.getenv("DB_CLUSTER")

    try:
        client = boto3.client('redshift')
        creds = client.get_cluster_credentials(  # Lambda needs these permissions as well DataAPI permissions
            DbUser=user,
            DbName=db,
            ClusterIdentifier=cluster,
            DurationSeconds=3600) # Length of time access is granted
    except Exception as ERROR:
        print("Credentials Issue: " + str(ERROR))
        sys.exit(1)

    print('got credentials')

    try:
        conn = psycopg2.connect(
            dbname=db,
            user=creds["DbUser"],
            password=creds["DbPassword"],
            port=port,
            host=host)
    except Exception as ERROR:
        print("Connection Issue: " + str(ERROR))
        sys.exit(1)

    print('connected')

    # Read raw csv data
    try: 
        file_name = get_file_name(bucket='cafe-transactions',
                                  location='isle of wight',
                                  date_string=None)
    except Exception as ERROR:
        print ("Couldn't extract from S3 files")
        print (str(ERROR))
    print(file_name)
    try:
        data = read_csv_file_from_s3(bucket='cafe-transactions', key=file_name)
        print('Read data from csv')
        raw_transactions = output_raw_transactions(data)
        print('Read raw transactions')
    except Exception as ERROR:
        print ("Couldn't extract from S3 files")
        print (str(ERROR))

    # Clean Transactions & Basket data
    try: 
        clean_transaction_list = clean_transactions(raw_transactions)
        print('Clean transactions')
        basket_list = update_raw_basket(clean_transaction_list)
        print('Read baskets')
        clean_basket_list = clean_basket_items(basket_list)
        print('Clean baskets')
    except Exception as ERROR:
        print ("Couldn't transform S3 files")
        print (ERROR)
    
    # Write transactions and basket to database
    with conn.cursor() as cursor:
        psycopg2.extras.execute_values(cursor, """
            INSERT INTO transactions_g3 VALUES %s;
        """, [(
            transaction.unique_id,
            transaction.date,
            transaction.first_name,
            transaction.total,
            transaction.location   
        ) for transaction in clean_transaction_list])
        conn.commit()
    print ("Transactions written to database")
    
    with conn.cursor() as cursor:
        psycopg2.extras.execute_values(cursor, """
            INSERT INTO basket_g3 (transaction_id, item, cost) VALUES %s;
        """, [(
            basket.trans_id,
            basket.item,
            basket.cost  
        ) for basket in clean_basket_list])
        conn.commit()
    print ("Basket Items written to database")
