import json
import datetime

def load_servers(filename):
    with open(filename, "r") as f:
        return json.load(f)
    
def generate_report(servers):
    report = []
    report.append("=" * 40)
    report.append("SERVER HEALTH REPORT")
    report.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 40)

    running = [s for s in servers if s["status"] == "running"]
    stopped = [s for s in servers if s["status"] == "stopped"]

    report.append(f"\nTotal servers: {len(servers)}")
    report.append(f"Running: {len(running)}")
    report.append(f"stopped: {len(stopped)}")

    report.append("\n--- Running servers ---")
    for s in running:
        report.append(f"    {s['name']} | {s['type']} | {s['region']}")

    if stopped:
        report.append("\n--- Stopped servers (ACTION NEEDED) ---")
        for s in stopped:
            report.append(f"{s['name']} | {s['type']} | {s['region']}")

    report.append("=" * 40)
    return "\n".join(report)

servers = load_servers("servers.json")
report = generate_report(servers)

print(report)

#save report to file
report_name = f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(report_name, "w") as f:
    f.write(report)

print(f"\nReport saved to {report_name}")
