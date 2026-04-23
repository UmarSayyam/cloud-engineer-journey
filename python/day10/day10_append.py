import datetime

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    with open("server.log", "a") as f:
        f.write(log_entry)

    print(log_entry.strip())

log("Server restarted")
log("New connection from 192.168.1.1")
log("CPU usage: 45%")
log("Disk usage: 60%")

#read full log
print("\n--- Full log ---")
with open("server.log", "r") as f:
    print(f.read())