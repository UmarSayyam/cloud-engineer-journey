# Why file handling matters in cloud engineering
# As a cloud engineer you'll constantly:

# Read config files to get server settings
# Write log files to track what your scripts did
# Parse CSV/JSON files from AWS cost reports
# Generate reports automatically




# Write to a file
# with open("file.txt", "w") as f:
#     f.write("Hello World")

# #Read a file
# with open("file.txt", "r") as f:
#     content = f.read()
#     print(content)

# #Append a file
# with open("file.txt", "a") as f:
#     f.write("\nNew line added")



#write a server log file
with open("server.log", "w") as f:
    f.write("Server started\n")
    f.write("connected to database\n")
    f.write("listning on port80\n")
    f.write("health check passed\n")

print("log file created")

#read it back
with open("server.log", "r") as f:
    content = f.read()
    print(content)

#read line by line
print("--- line by line ---")
with open("server.log", "r") as f:
    for line in f:
        print(line.strip())
