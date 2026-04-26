# import boto3
# import json

# ec2 = boto3.client('ec2', region_name='ap-south-1')

# with open('vpc_resources.json', 'r') as f:
#     r = json.load(f)

# print("=== Cleaning up VPC resources ===\n")

# print("1. Detaching and deleting IGW...")
# ec2.detach_internet_gateway(InternetGatewayId=r['igw_id'], VpcId=r['vpc_id'])
# ec2.delete_internet_gateway(InternetGatewayId=r['igw_id'])
# print(f"   Deleted: {r['igw_id']}")

# print("2. Deleting subnets...")
# ec2.delete_subnet(SubnetId=r['public_subnet_id'])
# ec2.delete_subnet(SubnetId=r['private_subnet_id'])
# print("   Both subnets deleted")

# print("3. Deleting route table...")
# rt = ec2.describe_route_tables(RouteTableIds=[r['public_rt_id']])
# for assoc in rt['RouteTables'][0].get('Associations', []):
#     if not assoc.get('Main'):
#         ec2.disassociate_route_table(AssociationId=assoc['RouteTableAssociationId'])
# ec2.delete_route_table(RouteTableId=r['public_rt_id'])
# print(f"   Deleted: {r['public_rt_id']}")

# print("4. Deleting security group...")
# ec2.delete_security_group(GroupId=r['sg_id'])
# print(f"   Deleted: {r['sg_id']}")

# print("5. Deleting VPC...")
# ec2.delete_vpc(VpcId=r['vpc_id'])
# print(f"   Deleted: {r['vpc_id']}")

# print("\n=== Cleanup complete! No charges ✅ ===")


# import boto3, json
# ec2 = boto3.client('ec2', region_name='ap-south-1')
# with open('vpc_resources.json') as f:
#     r = json.load(f)
# ec2.delete_vpc(VpcId=r['vpc_id'])
# print(f"VPC deleted: {r['vpc_id']} ✅")



import boto3, json

ec2 = boto3.client('ec2', region_name='ap-south-1')

with open('vpc_resources.json') as f:
    r = json.load(f)

ec2.delete_vpc(VpcId=r['vpc_id'])
print(f"VPC deleted ✅")