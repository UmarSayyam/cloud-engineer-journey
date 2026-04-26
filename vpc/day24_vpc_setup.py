import boto3
import json

ec2 = boto3.client('ec2', region_name='ap-south-1')

def tag(resource_id, name):
    ec2.create_tags(
        Resources=[resource_id],
        Tags=[{'Key': 'Name', 'Value': name}]
    )

print("=== Day 24: Building a VPC from scratch ===\n")

# Step 1: Create VPC
print("1. Creating VPC...")
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = vpc['Vpc']['VpcId']
tag(vpc_id, 'umar-custom-vpc')
ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
print(f"   VPC created: {vpc_id}")

# Step 2: Create public subnet
print("\n2. Creating public subnet...")
public_subnet = ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock='10.0.1.0/24',
    AvailabilityZone='ap-south-1a'
)
public_subnet_id = public_subnet['Subnet']['SubnetId']
tag(public_subnet_id, 'umar-public-subnet')
ec2.modify_subnet_attribute(
    SubnetId=public_subnet_id,
    MapPublicIpOnLaunch={'Value': True}
)
print(f"   Public subnet: {public_subnet_id}")

# Step 3: Create private subnet
print("\n3. Creating private subnet...")
private_subnet = ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock='10.0.2.0/24',
    AvailabilityZone='ap-south-1b'
)
private_subnet_id = private_subnet['Subnet']['SubnetId']
tag(private_subnet_id, 'umar-private-subnet')
print(f"   Private subnet: {private_subnet_id}")

# Step 4: Create Internet Gateway
print("\n4. Creating Internet Gateway...")
igw = ec2.create_internet_gateway()
igw_id = igw['InternetGateway']['InternetGatewayId']
tag(igw_id, 'umar-igw')
ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
print(f"   IGW created and attached: {igw_id}")

# Step 5: Create public route table
print("\n5. Creating route table...")
public_rt = ec2.create_route_table(VpcId=vpc_id)
public_rt_id = public_rt['RouteTable']['RouteTableId']
tag(public_rt_id, 'umar-public-rt')
ec2.create_route(
    RouteTableId=public_rt_id,
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=igw_id
)
ec2.associate_route_table(
    RouteTableId=public_rt_id,
    SubnetId=public_subnet_id
)
print(f"   Route table created: {public_rt_id}")
print(f"   Route added: 0.0.0.0/0 → IGW")

# Step 6: Create security group
print("\n6. Creating security group...")
sg = ec2.create_security_group(
    GroupName='umar-vpc-sg',
    Description='Security group for umar custom VPC',
    VpcId=vpc_id
)
sg_id = sg['GroupId']
tag(sg_id, 'umar-vpc-sg')
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)
print(f"   Security group created: {sg_id}")

# Summary
print("\n=== VPC BUILD COMPLETE ===")
print(f"VPC ID:              {vpc_id}")
print(f"Public Subnet ID:    {public_subnet_id}")
print(f"Private Subnet ID:   {private_subnet_id}")
print(f"IGW ID:              {igw_id}")
print(f"Route Table ID:      {public_rt_id}")
print(f"Security Group ID:   {sg_id}")

# Save to file
resources = {
    "vpc_id": vpc_id,
    "public_subnet_id": public_subnet_id,
    "private_subnet_id": private_subnet_id,
    "igw_id": igw_id,
    "public_rt_id": public_rt_id,
    "sg_id": sg_id
}
with open('vpc_resources.json', 'w') as f:
    json.dump(resources, f, indent=2)
print("\nResources saved to vpc_resources.json ")