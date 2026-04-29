def lambda_handler(event, context):
    print("Lambda function started")
    name = event.get('name', 'World')
    message = f"Hello {name} from Lambda!"
    print(message)
    result = {
        'statusCode': 200,
        'body': message
    }
    return result