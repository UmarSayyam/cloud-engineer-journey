import boto3
import json

iam = boto3.client('iam')

# Trust policy — allows EC2 to assume this role
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

# Create the role
try:
    response = iam.create_role(
        RoleName='EC2-S3-ReadOnly-Role',
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description='Allows EC2 instances to read from S3'
    )
    print(f"Role created: {response['Role']['RoleName']}")
    print(f"Role ARN: {response['Role']['Arn']}")
except iam.exceptions.EntityAlreadyExistsException:
    print("Role already exists!")

# Attach S3 read only policy to role
iam.attach_role_policy(
    RoleName='EC2-S3-ReadOnly-Role',
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
)
print(f"S3ReadOnly policy attached to role!")

# List roles
print("\n=== Your IAM Roles ===")
response = iam.list_roles()
for role in response['Roles']:
    if not role['RoleName'].startswith('AWS'):
        print(f"  {role['RoleName']}")
        print(f"  ARN: {role['Arn']}")