import boto3

lambda_client = boto3.client('lambda', region_name = 'ap-south-1')
iam = boto3.client('iam', region_name = 'ap-south-1')

lambda_client.delete_function(FunctionName='umar-lambda-demo')
print("DELETED")

iam.detach_role_policy(
    RoleName = 'umar-lambda-role',
    PolicyArn = 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
)
iam.delete_role(RoleName ='umar-lambda-role')
print("Role Deleted")

