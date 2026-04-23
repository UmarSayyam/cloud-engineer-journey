import json

def load_config(filename):
    with open(filename, "r") as f:
        return json.load(f)
    
config = load_config("config.json")

print("Configuration loaded:")
print(f"  Region: {config['region']}")
print(f"  Instance type: {config['instance_type']}")
print(f"  Max instances: {config['max_instances']}")

#use config values
print(f"\nWould launch {config['instance_type']} in {config['region']}")
print(f"Using key: {config['key_name']}")