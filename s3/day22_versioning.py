import boto3

s3 = boto3.client('s3', region_name='ap-south-1')
bucket_name = 'umar-cloud-engineer-2026'

#enable versioning on the bucket
s3.put_bucket_versioning(Bucket=bucket_name, VersioningConfiguration={'Status': 'Enabled'})
print(f"Versioning enabled on bucket '{bucket_name}'.")

#upload same file 3 times with different content
versions = [
    'Version 1 - Initial content',
    'Version 2 - Updated content',
    'Version 3 - Final content'
]

for i, content in enumerate(versions, 1):
    s3.put_object(
        Bucket=bucket_name,
        Key='versioned_file.txt',
        Body=content
    )
    print(f"Uploaded: {content}")

#List all versions
print(f"\nAll versions of 'versioned_file.txt' in bucket '{bucket_name}':")
response = s3.list_object_versions(Bucket=bucket_name, Prefix='versioned_file.txt')
for version in response['Versions']:
    print(f"    Version ID: {version['VersionId'][:20]}...")
    print(f"    Size: {version['Size']}bytes")
    print(f"    Is Latest: {version['IsLatest']}")
    print(f"    Last Modified: {version['LastModified'].strftime('%Y-%m-%d %H:%M:%S')}\n")
    print()
