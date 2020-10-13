import boto3

#Create a function for sending sqs messages
def send_sqs(message):
    sqs = boto3.client('sqs')
    queue_url = "This is the URL"
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageBody=(message)
    )
    return response

#Add this into main function start (event,contect):
>>this is the dictionary of stuff from csv
try:
    for key, value in dictionary.list():
        message = (key + ' : ' + value)
        response = send_sqs(message)
        print(response['MessageId'])
