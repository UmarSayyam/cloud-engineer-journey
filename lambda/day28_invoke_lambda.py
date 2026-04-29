import boto3
import json

lambda_client = boto3.client('lambda', region_name='ap-south-1')

print("=== Invoking Lambda ===")

response = lambda_client.invoke(
    FunctionName = 'umar-lambda-demo',
    InvocationType = 'RequestResponse',
    Payload = json.dumps({'name': 'umar'})
)

result = json.loads(response['Payload'].read())
print(f"Status: {response['StatusCode']}")
print(f"Response: {result}")