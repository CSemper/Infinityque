import json
import logging

import boto3

from sqs_messaging import send_sqs_message

logging.getLogger().setLevel(logging.INFO)

def start(event, context):
    # Remove this code!!!
    stream_name = 'store-stream'
    kinesis_client = boto3.client('kinesis', region_name='eu-west-1')
    response = kinesis_client.describe_stream(StreamName=stream_name)
    shard_id = response['StreamDescription']['Shards'][0]['ShardId']
    shard_iterator = kinesis_client.get_shard_iterator(StreamName=stream_name,
                                                      ShardId=shard_id,
                                                      ShardIteratorType='TRIM_HORIZON')

    kinesis_shard_iterator = shard_iterator['ShardIterator']

    record_response = kinesis_client.get_records(ShardIterator=kinesis_shard_iterator,Limit=5)
 
    record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'],Limit=5)
    # Get data from kinesis stream
    try:
        kinesis_stream = event['Records']
        logging.info({'event': kinesis_stream})
    except Exception as ERROR:
        logging.error({'event[Records] not found': event})
    kinesis_stream = record_response['Records']
    
    counter = 0
    for data_record in kinesis_stream:
        # Convert binary string to python list
        row_binary = data_record['Data']
        logging.info({'binary row': row_binary})
        row_string = row_binary.decode('utf-8')
        logging.info({'decoded row': row_string})
        row = json.loads(row_string)
        logging.info({'row': row})
        # Create unique identifier
        identifier = row[1].ljust(12, 'a')
        # Convert list to dictionary
        raw_transaction = {
            'date': row[0],
            'location': row[1],
            'customer_name': row[2],
            'basket': row[3],
            'pay_amount': row[4],
            'payment_method': row[5],
            'ccn': row[6],
            'id_number': counter,
            'identity': identifier
        }
        logging.info({'raw transaction': raw_transaction})
        counter += 1
        # Convert dictionary to json list
        message = json.dumps([raw_transaction])
        # Send row SQS
        queue_name = 'Group3SQSKinesistoTransorm'
        queue_url = 'https://sqs.eu-west-1.amazonaws.com/579154747729/Group3SQSKinesistoTransorm'
        try:
            send_sqs_message(
                message,
                queue_name=queue_name,
                queue_url=queue_url
            )
            logging.info({'message': message})
        except Exception as ERROR:
            logging.error({'message failed': message})
            logging.error(ERROR)
