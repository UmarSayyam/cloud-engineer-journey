import boto3

#connect to ec2 in mumbai region
ec2 = boto3.client('ec2', region_name='ap-south-1')

#list all ec2 instances
response = ec2.describe_instances()

reservations = response['Reservations']

if len(reservations) == 0:
    print("NO Ec2 instances Found")
else:
    print(f"Found {len(reservations)} instance(s):\n")
    for r in reservations:
        for instance in r['Instances']:
            print(f"Instance ID:    {instance['InstanceId']}")
            print(f"State:  {instance['State']['Name']}")
            print(f"Type:   {instance['InstanceType']}")
            print(f"Region:     ap-south-1")
            if 'PublicIpAddress' in instance:
                print(f"Public IP:  {instance['PublicIpAddress']}")
            print("-" * 30)