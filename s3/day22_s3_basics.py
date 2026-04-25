import boto3
import json

s3 = boto3.client('s3', region_name='ap-south-1')

# list all buckets
response = s3.list_buckets()
print("Your S3 Buckets are :")
for bucket in response['Buckets']:
    print(f"  {bucket['Name']} - created {bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S')}")

#check if our bucket exists
bucket_name = "umar-cloud-engineer-2026"
print(f"\nChecking if bucket '{bucket_name}' exists...")

try:
    s3.head_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' exists.")
except:
    print(f"Bucket '{bucket_name}' does not exist. - creating it now...")
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
    print(f"Bucket '{bucket_name}' created successfully.")

#upload multiple files to the bucket
files = {
    'index.html': '<html><body><h1>Welcome to my S3 bucket!</h1></body></html>',
    'about.html': '<html><body><h1>About Me</h1><p>This is a sample about page.</p></body></html>',
    'style.css': 'body { font-family: Arial, sans-serif; background-color: #f0f0f0; } h1 { color: #333; }',
    'data.json': '{"name": "Umar", "age": 23, "city": "Lahore"}'
}

print(f"\nUploading files to bucket '{bucket_name}'...")
for filename, content in files.items():
    s3.put_object(Bucket=bucket_name, Key=filename, Body=content)
    print(f"  Uploaded '{filename}'")

#list all objects in the bucket
print(f"\nObjects in bucket '{bucket_name}':")
response = s3.list_objects_v2(Bucket=bucket_name)
for obj in response['Contents']:
    print(f"  {obj['Key']} - size: {obj['Size']} bytes")
    