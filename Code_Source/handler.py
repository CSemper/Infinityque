import psycopg2
import sys
import os

import boto3
from dotenv import load_dotenv
from transform import clean_transaction_list, clean_transactions, update_raw_basket, raw_basket_list
from transform import clean_basket_items, clean_basket_list, raw_transaction_list
from read import return_most_recent_file, read_csv_file_from_s3, output_raw_transactions
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

    """Read latest CSV File"""
    try: 
        last_file = return_most_recent_file(bucket='cafe-transactions')
        data = read_csv_file_from_s3(bucket='cafe-transactions', key=last_file)
        output_raw_transactions(data)
    except Exception as ERROR:
        print ("Couldn't extract from S3 files")
        print (str(ERROR))

    """Clean Transactions & Basket"""
    try: 
        clean_transactions()
        update_raw_basket()
        clean_basket_items()
    except Exception as ERROR:
        print ("Couldn't transform S3 files")
        print (ERROR)

    """Write Transactions and Basket Items to Database"""
    try:
        for transaction in clean_transaction_list:
            cursor = conn.cursor()
            sql = "INSERT INTO transactions (unique_id, date, first_name, total) VALUES (%s ,%s, %s, %s)"
            cursor.execute(sql, (transaction.unique_id, transaction.date, transaction.first_name, transaction.total))
            cursor.close()
            conn.commit()
        print ("transactions entered into database")
        for entry in clean_basket_list:
            cursor = conn.cursor()
            command = "INSERT INTO basket (transaction_id, item, cost) VALUES (%s, %s, %s)"
            cursor.execute(command, (entry.trans_id, entry.item, entry.cost))
            cursor.close()
            conn.commit()
        print ("basket items entered into database")
        conn.close()
    except Exception as ERROR:
        print ("Couldn't load S3 files to Redshift Database")
        print (str(ERROR))


# con = psycopg2.connect(
#     "dbname=dev host=redshift-cluster-1.cduzkj2qjmlq.eu-west-2.redshift.amazonaws.com port=5439 user=test password=Password1")
