import psycopg2
import sys
import os

import boto3
from dotenv import load_dotenv
from transform import clean_transactions, update_raw_basket
from transform import clean_basket_items, raw_transaction_list
from read import return_most_recent_file, read_csv_file_from_s3, output_raw_transactions
from read import create_sql_transactions_string, create_sql_basket_string
from classes import Transaction, Basket

load_dotenv()

def start(event, context):
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

    # Read latest CSV File
    try: 
        last_file = return_most_recent_file(bucket='cafe-transactions')
        print(last_file)
        data = read_csv_file_from_s3(bucket='cafe-transactions', key=last_file)
        print('Read data from csv')
        raw_transactions = output_raw_transactions(data)
        print('Read raw transactions')
    except Exception as ERROR:
        print ("Couldn't extract from S3 files")
        print (str(ERROR))

    # Clean Transactions & Basket
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

    """Write Transactions and Basket Items to Database"""
    try:
        cursor = conn.cursor()
        # Add transactions to table
        sql_transactions = create_sql_transactions_string(clean_transaction_list)
        cursor.execute(sql_transactions)
        print('Wrote transactions to table')
        conn.commit()
        # Add baskets to table
        sql_baskets = create_sql_basket_string(clean_basket_list)
        cursor.execute(sql_baskets)
        print('Wrote baskets to table')
        conn.commit()
    except Exception as ERROR:
        print ("Couldn't load S3 files to Redshift Database")
        print (str(ERROR))
    finally:
        cursor.close()
        conn.close()

# con = psycopg2.connect(
#     "dbname=dev host=redshift-cluster-1.cduzkj2qjmlq.eu-west-2.redshift.amazonaws.com port=5439 user=test password=Password1")
