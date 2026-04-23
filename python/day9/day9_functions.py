#functions - resuable blocks of code
def greet(name):
    print(f"hello {name}, welcome to cloud engineering!")

greet("umar")
greet("AWS")

#function with return values
def add(a,b):
    return a+b

result = add(10, 5)
print(f"10 + 5 = {result}")

#function with default values
def describe_server(name, status="running", region="ap-south-1"):
    print(f"Server: {name} | Status: {status} | Region: {region}")

describe_server("web-01")
describe_server("db-01", status="stopped")
describe_server("cache-01", status="pending", region="us-east-1")

#function that return a dictionary
def create_instance(name, instance_type, region):
    return{
        "name": name,
        "type": instance_type,
        "region": region,
        "status": "pending"
    }

server = create_instance("web-01", "t2.micro", "ap-south-1")
print(server)
print(f"Launched {server['name']} in {server['region']}")