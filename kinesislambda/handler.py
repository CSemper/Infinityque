import json, logging, os
import boto3

from sqs_messaging import send_message_list_to_sqs, split_long_list

# logging.getLogger().setLevel(logging.ERROR)

def start(event, context):
    stream_name = 'store-stream'
    kinesis_client = boto3.client('kinesis', region_name='eu-west-1')
    response = kinesis_client.describe_stream(StreamName=stream_name)
    shard_id = response['StreamDescription']['Shards'][0]['ShardId']
    shard_iterator = kinesis_client.get_shard_iterator(StreamName=stream_name,
                                                      ShardId=shard_id,
                                                      ShardIteratorType='TRIM_HORIZON')

    kinesis_shard_iterator = shard_iterator['ShardIterator']

    record_response = kinesis_client.get_records(ShardIterator=kinesis_shard_iterator,Limit=5)
 
    # while 'NextShardIterator' in record_response:
    #     # read up to 100 records at a time from the shard number
    record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'],Limit=5)
    print (record_response['Records'])
    print ("Okay")
    print (record_response['Records']['Data'])
        
# # wait for 1 seconds before looping back around to see if there is any more data to read
# time.sleep(1)
        
        
# for line in csv_reader:
#         try:
#             raw_transaction = {
#                 'date': line[0],
#                 'location': line[1],
#                 'customer_name': line[2],
#                 'basket': line[3],
#                 'pay_amount': line[4],
#                 'payment_method': line[5],
#                 'ccn': line[6],
#                 'id_number': counter,
#                 'identity': identifier
#             }