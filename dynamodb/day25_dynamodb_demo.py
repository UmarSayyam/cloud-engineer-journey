from decimal import Decimal
from boto3.dynamodb.conditions import Key
import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
client = boto3.client('dynamodb', region_name='ap-south-1')

print("===Day 25: Dynamo DB hands on practice")

print("1. Creating a table...")
try:
    table= dynamodb.create_table(
        TableName = 'umar-users',
        KeySchema = [
            {'AttributeName': 'user_id', 'KeyType': 'HASH'},
            {'AttributeName': 'email', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions = [
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
            {'AttributeName': 'email', 'AttributeType': 'S'}
        ],
        BillingMode = 'PAY_PER_REQUEST'
    )
    table.wait_until_exists()
    print(f" Table created: umar-users")


except client.exceptions.ResourceInUseException:
    print(f"Table with same name already exists: {'TableName'} ")
    table = dynamodb.Table('umar-users')

# Step:2 Inserting Items
print(" Inserting Items.....")
users = [
    {
        'user_id': 'u001',
        'email': 'ali@example.com',
        'name': 'Ali Hassan',
        'age': Decimal('25'),
        'city': 'Lahore',
        'skills': ['Python', 'AWS']
    },
   {
        'user_id': 'u002',
        'email': 'sara@example.com',
        'name': 'Sara Khan',
        'age': Decimal('28'),
        'city': 'Karachi',
        'skills': ['JavaScript', 'React']
    },
    {
        'user_id': 'u003',
        'email': 'umar@example.com',
        'name': 'Umar Sayyam',
        'age': Decimal('23'),
        'city': 'Lahore',
        'skills': ['Python', 'AWS', 'Docker',]
        }
    
]
for user in users:
    table.put_item(Item=user)
    print(f"    Inserted: {user['name']}")


# Step 3: Get a single item
print("Getting sinlge items from database")

response = table.get_item(
    Key = {
        'user_id' : 'u003',
        'email': 'umar@example.com'
    }
)
item = response['Item']

print(f"Name: {item['name']}, city: {item['city']}")
print(f"Skills: {item['skills']}")

#update an item
print("step4. updating an item")
update = table.update_item(
    Key = {
        'user_id': 'u003',
        'email': 'umar@example.com'
    },
    UpdateExpression = 'SET city = :new_city',
    ExpressionAttributeValues = {
        ':new_city': 'Lahore- cloud engineer'
    }
)
print("city updated sucessfully")


# Scan all table
print("Step5: scanning whole table")
response = table.scan()
items = response['Items']
print(f"Total number of items in table are: {len(items)}")

for item in items:
    print(f"    {item['name']} | {item['city']} | {item['email']}")


#query by partition key
print("Step6: query by partition")
response = table.query(
    KeyConditionExpression=Key('user_id').eq('u001')
)
item = response['Items']
print(f"Query result: {item[0]['name']}")


# Delete Item
print("step7: Deleting an item")
table.delete_item(
    Key={
        'user_id': 'u002',
        'email': 'sara@example.com'
    }
)
print("Deleted succesfully")



#checking sara
print("below is checking if sara exists anymore")
response = table.query(
    KeyConditionExpression=Key('user_id').eq('u002')
)
item = response['Items']
print(f"query for sara: {item}")