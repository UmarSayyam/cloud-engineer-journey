# url = "https://httpbingo.org/post"

import requests
import json

def create_server(name, instance_type, region):
    url = "https://httpbingo.org/post"

    payload = {
        "name": name,
        "instance_type": instance_type,
        "region": region,
        "status": "pending"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer my-fake-token"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        print(f"Server creation request sent!")
        print(f"Status: {response.status_code}")
        print(f"Data sent: {data['json']}")
        print(f"Headers sent: {data['headers']['Authorization']}")

    except Exception as e:
        print(f"Failed to create server: {e}")

create_server("web-01", "t2.micro", "ap-south-1")
