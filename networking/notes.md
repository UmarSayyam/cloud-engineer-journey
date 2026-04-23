# Networking Notes

## Key concepts
- IP addresses: private (192.168.x.x) vs public
- DNS: translates domain names to IP addresses
- TCP: reliable, connection-based (HTTP, SSH)
- UDP: fast, connectionless (DNS, video)
- Ports: 22 SSH, 80 HTTP, 443 HTTPS, 3306 MySQL

## Tools used
- ping — test connectivity
- nslookup, dig — DNS lookup
- traceroute — trace network path
- nc (netcat) — test port connectivity
- ss — show open ports and connections
- curl — HTTP requests from terminal
- wget — download files from terminal

## AWS Networking
- VPC: your private network in AWS
- Subnets: /24 = 254 hosts, /16 = 65534 hosts
- Security Groups = cloud firewall (allow/deny ports)
- NAT Gateway: lets private servers reach internet
- ELB: distributes traffic across multiple servers
