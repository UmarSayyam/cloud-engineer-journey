import requests

#call a public api no key needed
response = requests.get("https://api.github.com")

print(f"Status code: {response.status_code}")
print(f"Response type: {type(response.json())}")
print()

data = response.json()
print(f"Current user URL: {data['current_user_url']}")
print(f"Repository URL: {data['repository_url']}")
print(f"Issues URL: {data['issues_url']}")