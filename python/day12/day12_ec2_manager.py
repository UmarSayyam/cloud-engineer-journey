import boto3

ec2 = boto3.client('ec2', region_name='ap-south-1')

def list_instances():
    response = ec2.describe_instances()
    print("\n--- EC2 Instances ---")
    for r in response ['Reservations']:
        for i in r ['Instances']:
            print(f"ID:     {i['InstanceId']}")
            print(f"State:      {i['State']['Name']}")
            print(f"Type:       {i['InstanceType']}")
            print("-" * 30)

def start_instance(instance_id):
    print(f"\nStarting {instance_id}...")
    ec2.start_instances(InstanceIds=[instance_id])
    print(f"\nStart command sent!")

def stop_instance(instance_id):
    print(f"\nStopping {instance_id}...")
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"\nStop command sent!")

def get_instance_state(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    state = response['Reservations'][0]['Instances'][0]['State']['Name']
    print(f"\nInstance {instance_id} is: {state}")
    return state

#List all instances
list_instances

#get state of your instance
instance_id = "i-089270d44e3f95ba1"
get_instance_state(instance_id)

#Start it
start_instance(instance_id)

#check state again
import time
print(f"\nWaiting 5 seconds...")
time.sleep(5)
get_instance_state(instance_id)    

#Stop it to save hours and cost and save free tier
stop_instance(instance_id)
print("\n waiting 5 seconds...")
time.sleep(5)
get_instance_state(instance_id)