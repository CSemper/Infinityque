import boto3
import json

def send_dict_to_sqs(json_data):
    client= boto3.resource('sqs')

    queue= client.get_queue_by_name(QueueName='Group3SQSTransformtoLoad')
    queue_url = 'https://sqs.eu-west-1.amazonaws.com/579154747729/Group3SQSTransformtoLoad'
        
    response = queue.send_message(QueueUrl = queue_url, MessageBody = json_data)

    print(response['MessageId'])