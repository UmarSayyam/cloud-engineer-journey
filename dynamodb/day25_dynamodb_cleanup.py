import boto3

#deleting dynamodb table
dynamodb = boto3.resource('dynamodb', region_name = 'ap-south-1')
table = dynamodb.Table('umar-users')
table.delete()
print("table deleted succesfully")