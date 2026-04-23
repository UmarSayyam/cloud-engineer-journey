import json

#create a server inventory
servers = [
    {"name": "web-01", "type": "t2.micro", "region": "ap-south-1", "status": "running"},
    {"name": "web-02", "type": "t2.micro", "region": "ap-south-1", "status": "running"},
    {"name": "db-01", "type": "t2.medium", "region": "ap-south-1", "status": "running"},
    {"name": "cache-01", "type": "t2.small", "region": "us-east-1", "status": "stopped"},
]

#write to json file
with open("servers.json", "w") as f:
    json.dump(servers, f, indent=4)

print("servers.json created")

#Read it back
with open("servers.json", "r") as f:
    loaded = json.load(f)

print(f"Total servers: {len(loaded)}")

#filter running servers
running = [s for s in loaded if s["status"] == "running"]
print(f"Running servers: {len(running)}")

for server in running:
    print(f"{server['name']} - {server['type']} - {server['region']}")

#filter stopped servers
stopped = [s for s in loaded if s["status"] == "stopped"]
print(f"Stopped servers: {len(stopped)}")
for server in stopped:
    print(f"{server['name']} - {server['type']}")
    