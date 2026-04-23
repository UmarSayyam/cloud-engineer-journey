import requests

def safe_api_call(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"Request timed out: {url}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"Could not connect to: {url}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return None
    
#Test with good URL
print("Testing good URL:")
data = safe_api_call("https://api.github.com")
if data:
    print(f"Success! Got {len(data)} endpoints")

#Test with bad URL
print("\nTesting 404 URl: ")
data = safe_api_call("https://api.github.com/thisdoesnotexist")
if not data:
    print("Request failed, Handeled gracefully")
    
#Test with fake domain
print("\nTesting fake domain:")
data = safe_api_call("https://thisfakedomain12345abc.com")
if not data:
    print("Connection error handeled gracefully")