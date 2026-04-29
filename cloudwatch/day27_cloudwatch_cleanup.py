import boto3

cloudwatch = boto3.client('cloudwatch', region_name = 'ap-south-1')
cloudwatch.delete_alarms(AlarmNames=['umar-cpu-alarm'])
print("Alarm Deleted.")