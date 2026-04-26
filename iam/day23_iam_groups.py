import boto3
import json

iam = boto3.client('iam')

# Create a developer group
group_name = "CloudEngineers"

try:
    iam.create_group(GroupName=group_name)
    print(f"Group '{group_name}' created!")
except iam.exceptions.EntityAlreadyExistsException:
    print(f"Group '{group_name}' already exists!")

# Attach policies to the group
policies = [
    'arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess',
    'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
]

for policy in policies:
    iam.attach_group_policy(
        GroupName=group_name,
        PolicyArn=policy
    )
    policy_name = policy.split('/')[-1]
    print(f"Attached: {policy_name}")

# Add user to group
iam.add_user_to_group(
    GroupName=group_name,
    UserName='python-boto3-user'
)
print(f"\nAdded python-boto3-user to {group_name}")

# List group members
response = iam.get_group(GroupName=group_name)
print(f"\nMembers of {group_name}:")
for user in response['Users']:
    print(f"  {user['UserName']}")

# List group policies
response = iam.list_attached_group_policies(GroupName=group_name)
print(f"\nPolicies attached to {group_name}:")
for policy in response['AttachedPolicies']:
    print(f"  {policy['PolicyName']}")