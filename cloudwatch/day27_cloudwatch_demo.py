from datetime import datetime 
from datetime import timedelta
import boto3

cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')
print("=== Day27: CloudWatch ===")

print("Step1: listing ec2 metrics...")
response = cloudwatch.list_metrics(Namespace='AWS/EC2')
metrics = response['Metrics']
print(f"Total number of metrics: {len('metrics')}")

for metric in metrics[:5]:
    print(metric['MetricName'])

print("Step2: actual metric data (CPU usage)")
response = cloudwatch.get_metric_statistics(
    Namespace = 'AWS/EC2',
    MetricName = 'CPUUtilization',
    Dimensions = [{'Name': 'InstanceId', 'Value': 'i-089270d44e3f95ba1'}],
    StartTime = datetime.utcnow() - timedelta(hours=1),
    EndTime = datetime.utcnow(),
    Period = 300,
    Statistics = ['Average']
)
datapoints = response['Datapoints']
print(f"Number of datapoints are: {len(datapoints)}")

if datapoints:
    for dp in datapoints:
        print(f"    CPU: {dp['Average']}% at {dp['Timestamp']}")
else:
    print(" No data - instance was stopped")


print("Step3: Cloudwatch metric alarm...")
cloudwatch.put_metric_alarm(
    AlarmName = 'umar-cpu-alarm',
    MetricName = 'CPUUtilization',
    Namespace = 'AWS/EC2',
    Threshold = 80.0,
    ComparisonOperator = 'GreaterThanThreshold',
    EvaluationPeriods = 2,
    Period = 300,
    Statistic = 'Average',
    ActionsEnabled = False,
    AlarmDescription = 'Alert when CPU is high',
    Dimensions = [{'Name': 'InstanceId',
                   'Value': 'i-089270d44e3f95ba1'}]
)
print("Alarm created succesfully")