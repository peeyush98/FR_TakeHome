import boto3
import json
import psycopg2
import hashlib

aws_access_key_id = 'dummy-access-key'
aws_secret_access_key = 'dummy-secret-key'

# AWS SDK to use LocalStack
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1', aws_access_key_id='dummy-access-key', aws_secret_access_key='dummy-secret-key')

# URL of the SQS queue
queue_url = 'http://localhost:4566/000000000000/login-queue'

conn = psycopg2.connect(
    dbname='postgres', 
    user='postgres',
    password='postgres',
    host='localhost', 
    port=5432
)
cursor = conn.cursor()

# Receive a message from the queue

response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=['All'],
    MessageAttributeNames=['All'],
    MaxNumberOfMessages=1,
    VisibilityTimeout=0,
    WaitTimeSeconds=0
)


if 'Messages' in response:
    message = json.loads(response['Messages'][0]['Body'])
    print(message)
    
    # data transformation logic to mask PII fields (device_id and ip)
    transformed_data = {
        'user_id': [message['user_id']],
        'device_type': [message['device_type']],
        'masked_ip': [hashlib.sha256(message['ip'].encode()).hexdigest()], 
        'masked_device_id': [hashlib.sha256(message['device_id'].encode()).hexdigest()],
        'locale': [message['locale']],
        # 'app_version': str(message['app_version'])
    }
    
    # Inserting values into the table
    cursor.execute("""
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        transformed_data['user_id'],
        transformed_data['device_type'],
        transformed_data['masked_ip'],
        transformed_data['masked_device_id'],
        transformed_data['locale']
        # transformed_data['app_version']
    ))

    conn.commit()
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=response['Messages'][0]['ReceiptHandle'])

cursor.close()
conn.close()
