# 5 questions

#Q1: Create a variable called city 
#with value "Lahore" and print it in uppercase.

city = "lahore"
print(city.upper())

#Q2 — Create a list called clouds with 3 items: "AWS", "Azure", "GCP".
#  Add "Oracle" to it then print the length
clouds = ["AWS", "AZURE", "GCP"]
clouds.append("Oracle")
print(len(clouds))

#Q3 — Create a dictionary called server with keys name, region, status.
#  Print just the region value.
server = {
    "name": "web-01",
    "region": "ap-south-1",
    "status": "running"
}
print(server["region"])

#Q4 — Write a function called multiply that takes two numbers and returns their result.
#  Call it with 6 and 7 and print the result
def multiply(a, b):
    return a * b
result= multiply(6,7)
print(result)

#Q5 — Loop through this list and print only servers that contain "web"

servers = ["web-01", "db-01", "web-02", "cache-01", "web-03"]
for server in servers:
    if "web" in server:
        print(server)