import boto3
import json

#connect to s3
s3 = boto3.client('s3', region_name='ap-south-1')

#create a bucket
bucket_name = "umar-cloud-engineer-2026"

print(f"Creating Bucket: {bucket_name}")
s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'}
)
print(f"Bucket Created Succesfully")

#List all buckets
print(f"\nUploading File...")

s3.put_object(
    Bucket=bucket_name,
    Key='hello.txt',
    Body='Hello from pytho boto3! This is my first S3 upload'
)
print(f"File Uploaded")

#Read it back
response = s3.get_object(Bucket=bucket_name, Key='hello.txt')
content = response['Body'].read().decode('utf-8')
print(f"\nFile contents: {content}")