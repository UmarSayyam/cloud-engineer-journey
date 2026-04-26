import boto3
import json

iam = boto3.client('iam', region_name='ap-south-01')

#get surrent user info
print("Current IAM USer")
user = iam.get_user()
print(f"Username: {user['User']['UserName']}")
print(f"UserId: {user['User']['UserId']}")
print(f"ARN: {user['User']['Arn']}")
print(f"created: {user['User']['CreateDate'].strftime('%Y-%m-%d')}")

#list all iam users
print("\nList of IAM Users:")
users = iam.list_users()
for user in users['Users']:
    print(f"Username: {user['UserName']}, Created: {user['CreateDate'].strftime('%Y-%m-%d')}")

#list all iam groups
print("\nList of IAM Groups:")
groups = iam.list_groups()
if groups['Groups']:
    for g in groups['Groups']:
        print(f"    {g['GroupName']}")
else:
    print("No IAM Groups found.")

#liost of policies attatched to current user
print("\n---Policies attached to python-boto3-user---")
policies = iam.list_attached_user_policies(UserName='python-boto3-user')
for p in policies['AttachedPolicies']:
    print(f"{p['PolicyName']}")