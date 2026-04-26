import boto3
import json

iam = boto3.client('iam')

# Create a custom policy — S3 access to specific bucket only
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::umar-cloud-engineer-2026",
                "arn:aws:s3:::umar-cloud-engineer-2026/*"
            ]
        }
    ]
}

try:
    response = iam.create_policy(
        PolicyName='UmarS3BucketPolicy',
        Description='Access to umar-cloud-engineer-2026 bucket only',
        PolicyDocument=json.dumps(policy_document)
    )
    policy_arn = response['Policy']['Arn']
    print(f"Custom policy created!")
    print(f"Policy ARN: {policy_arn}")
    print(f"\nThis policy allows:")
    print(f"  - Read objects from umar-cloud-engineer-2026")
    print(f"  - Upload objects to umar-cloud-engineer-2026")
    print(f"  - Delete objects from umar-cloud-engineer-2026")
    print(f"  - List bucket contents")
    print(f"\nThis policy DENIES:")
    print(f"  - Access to ANY other S3 bucket")
    print(f"  - Creating or deleting buckets")
    print(f"  - Any EC2, IAM or other AWS actions")
except iam.exceptions.EntityAlreadyExistsException:
    print("Policy already exists!")