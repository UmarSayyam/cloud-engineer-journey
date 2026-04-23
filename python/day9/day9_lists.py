#Lists - ordered collection of items
servers = ["web-01", "web-02", "db-01", "cache-01"]

print(servers)
print(servers[0])
print(servers[-1])
print(len(servers))

#add and remove
servers.append("web-03")
print(servers)

servers.remove("cache-01")
print(servers)

#loop through list
for server in servers:
    print("Server:", server)

#check if item exists
if "db-01" in servers:
    print("Database in online")

#Dictionaries - key:value pairs
instance = {
    "id": "i-1234567890",
    "type": "t2.micro",
    "region": "ap-south-1",
    "status": "running",
    "ip": "13.234.117.136"
}

print(instance)
print(instance["type"])
print(instance["ip"])

#add a new key
instance["owner"] = "umar"
print(instance)

#loop through dictionary
for key, value in instance.items():
    print(f"{key}: {value}")
