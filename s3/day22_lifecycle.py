import boto3

s3 = boto3.client('s3', region_name='ap-south-1')
bucket_name = 'umar-cloud-engineer-2026'

#set lifecycle policy for the bucket
lifecycle_policy = {
    'Rules': [
        {
            'ID': 'Move to cheaper storage',
            'Status': 'Enabled',
            'Filter': {
                'Prefix': ''
            },
            'Transitions': [
                {
                    'Days': 30,
                    'StorageClass': 'STANDARD_IA'
                },
                {
                    'Days': 90,
                    'StorageClass': 'GLACIER'
                }
            ],
            'Expiration': {
                'Days': 365
            }
        }
    ]
}

s3.put_bucket_lifecycle_configuration(
    Bucket=bucket_name,
    LifecycleConfiguration=lifecycle_policy
)
print("Lifecycle policy set successfully for bucket:", bucket_name)
print("\nPolicy rules:")
print(" Day 0-30: Standard storage (frequent access)")
print(" Day 30-90: Standard IA storage (infrequent access, cheaper)")
print(" Day 90-365: Glacier storage (archival, very cheap)")
print(" Day 365: Automatically deleted")