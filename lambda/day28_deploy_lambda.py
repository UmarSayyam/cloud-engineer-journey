import boto3
import json
import zipfile
import os

iam = boto3.client('iam', region_name='ap-south-1')
lambda_client = boto3.client('lambda', region_name='ap-south-1')

print("=== DAY 28 Deploying Lambda===")

print("1. Creating ZIP file...")
zip_path = os.path.join(os.path.dirname(__file__), 'lambda_function.zip')
py_path = os.path.join(os.path.dirname(__file__), 'lambda_function.py')
with zipfile.ZipFile(zip_path, 'w') as z:
    z.write(py_path, 'lambda_function.py')
print("     ZIP created!")


print("2. Creating IAM role...")
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {
            "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
    }]
}

try:
    role = iam.create_role(
        RoleName = 'umar-lambda-role',
        AssumeRolePolicyDocument = json.dumps(trust_policy)
    )
    role_arn = role['Role']['Arn']
    print(role_arn)

except iam.exceptions.EntityAlreadyExistsException:
    role = iam.get_role(RoleName='umar-lambda-role')
    role_arn = role['Role']['Arn']
    print("   Role already exists")

# Attach basic Lambda execution policy
iam.attach_role_policy(
    RoleName='umar-lambda-role',
    PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
)
print("   Policy Attatched!")

print("3. Deploying Lambda function...")
with open(zip_path, 'rb') as f:
    zip_content = f.read()
try:
    response = lambda_client.create_function(
        FunctionName = 'umar-lambda-demo',
        Runtime = 'python3.12',
        Role = role_arn,
        Handler = 'lambda_function.lambda_handler',
        Code = {'ZipFile': zip_content},
        Description = 'My lambda function',
        Timeout = 30
    )
    print(f"    Function ARN: {response['FunctionArn']}")
except lambda_client.exceptions.ResourceConflictException:
    print("     Function Already exists")

print("     Lambda Deployed")