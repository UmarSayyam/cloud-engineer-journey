import json
import boto3
import urllib.parse
from datetime import datetime
from decimal import Decimal

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('file-analysis')

def lambda_handler(event, context):
    # Get bucket and file info from s3 event
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(record['s3']['object']['key'])

    print(f"Processing file: {key} from bucket: {bucket}")

    try:
        #read file from s3
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')

        #Analyse the file
        lines = content.split('\n')
        words = content.split()
        characters = len(content)

        #Save results to dynamoDB
        table.put_item(Item={
            'file_key': key,
            'bucket': bucket,
            'lines': Decimal(str(len(lines))),
            'words': Decimal(str(len(words))),
            'characters': Decimal(str(characters)),
            'processed_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'processed'
        })

        print(f"Analysis complete: {len(lines)} lines, {len(words)} words, {characters} chars")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'file': key,
                'lines': len(lines),
                'words': len(words),
                'characters': characters
            })
        }
    except Exception as e:
        print(f"Error processing {key}: {str(e)}")

        table.put_item(Item={
            'file_key': key,
            'bucket': bucket,
            'status': 'error',
            'error': str(e),
            'processed_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        })

        raise e 
