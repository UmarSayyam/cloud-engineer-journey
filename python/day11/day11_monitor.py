import requests
import json
import datetime

def check_url(url):
    try:
        response = requests.get(url, timeout=5)
        return {
            "url": url,
            "status": response.status_code,
            "healthy": response.status_code == 200,
            "response_time": response.elapsed.total_seconds()
        }
    except requests.exceptions.Timeout:
        return {"url": url, "status": "timeout", "healthy": False, "response_time": None}
    except requests.exceptions.ConnectionError:
        return {"url": url, "status": "connection_error", "healthy": False, "response_time": None}
    except Exception as e:
        return {"url": url, "status": str(e), "healthy": False, "response_time": None}

# List of URLs to monitor
urls = [
    "https://google.com",
    "https://github.com",
    "https://httpbin.org",
    "https://amazon.com",
    "https://thissitedoesnotexist12345.com",
]

print("=" * 50)
print("URL HEALTH MONITOR")
print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 50)

results = []
for url in urls:
    print(f"Checking {url}...")
    result = check_url(url)
    results.append(result)

print("\n--- Results ---")
healthy = 0
for r in results:
    status = "UP" if r["healthy"] else "DOWN"
    time = f"{r['response_time']:.2f}s" if r["response_time"] else "N/A"
    print(f"{status} | {r['url']} | {r['status']} | {time}")
    if r["healthy"]:
        healthy += 1

print(f"\nSummary: {healthy}/{len(urls)} sites healthy")

# Save results
with open("monitor_results.json", "w") as f:
    json.dump(results, f, indent=4)
print("Results saved to monitor_results.json")