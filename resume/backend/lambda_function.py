import json
import boto3
import os
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('resume-visitors')

def parse_device(user_agent):
    ua = user_agent.lower()
    if 'iphone' in ua:
        device = 'iPhone'
    elif 'ipad' in ua:
        device = 'iPad'
    elif 'android' in ua:
        device = 'Android'
    elif 'mac' in ua:
        device = 'Mac'
    elif 'windows' in ua:
        device = 'Windows'
    elif 'linux' in ua:
        device = 'Linux'
    else:
        device = 'Unknown'

    if 'chrome' in ua and 'edg' not in ua:
        browser = 'Chrome'
    elif 'firefox' in ua:
        browser = 'Firefox'
    elif 'safari' in ua:
        browser = 'Safari'
    elif 'edge' in ua:
        browser = 'Edge'
    else:
        browser = 'Unknown'

    return device, browser

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin':  '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        ip = event.get('requestContext', {}).get('identity', {}).get('sourceIp', 'unknown')
        user_agent = event.get('headers', {}).get('User-Agent', 'unknown')
        device, browser = parse_device(user_agent)
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        #update or create visitor record
        response = table.update_item(
            Key={'ip': ip},
            UpdateExpression= 'SET visit_count = if_not_exists(visit_count, :zero) + :one, device = :device, browser = :browser, last_visit = :timestamp, user_agent = :ua',
            ExpressionAttributeValues={
                ':zero': Decimal('0'),
                ':one': Decimal('1'),
                ':device': device,
                ':browser': browser,
                ':timestamp': timestamp,
                ':ua': user_agent[:200]
            },
            ReturnValues='ALL_NEW'
        )

        #Get total visitor count
        total = table.scan(Select='COUNT')['Count']

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'total_visitors': total,
                'your_visits': int(response['Attributes']['visit_count'])
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }