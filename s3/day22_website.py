import boto3
import json

s3 = boto3.client('s3', region_name='ap-south-1')
bucket_name = 'umar-cloud-engineer-2026'

#enable static website hosting
s3.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={
        'IndexDocument': {'Suffix': 'index.html'},
        'ErrorDocument': {'Key': 'error.html'}
    }
)
print(f"Static website hosting enabled for bucket: {bucket_name}")

#make bucket public
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }
    ]   
}
#disable block public access first
s3.delete_public_access_block(Bucket=bucket_name)
print("Public access block disabled for the bucket.")

#apply bucket policy
s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
print(f"Bucket policy applied to bucket: {bucket_name}")

#upload a proper index.html file to the bucket
html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Umar Sayyam — Cloud Engineer</title>
    <style>
        body { font-family: Arial; text-align: center; 
               padding: 50px; background: #232f3e; color: white; }
        h1 { color: #ff9900; }
        .badge { background: #ff9900; color: black; 
                 padding: 5px 15px; border-radius: 20px; margin: 5px; 
                 display: inline-block; }
    </style>
</head>
<body>
    <h1>Umar Sayyam</h1>
    <p>AWS Cloud Engineer in Training</p>
    <div>
        <span class="badge">Python</span>
        <span class="badge">AWS</span>
        <span class="badge">Linux</span>
        <span class="badge">Git</span>
    </div>
    <br>
    <p>Hosted on Amazon S3</p>
</body>
</html>"""
s3.put_object(Bucket=bucket_name, Key='index.html', Body=html_content, ContentType='text/html')
print("index.html uploaded to the bucket.")

website_url = f"http://{bucket_name}.s3-website-ap-south-1.amazonaws.com"
print(f"Your website is live at: {website_url}")