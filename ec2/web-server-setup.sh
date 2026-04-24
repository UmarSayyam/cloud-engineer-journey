#!/bin/bash
# EC2 Web Server Setup Script
# Run this on a fresh Ubuntu EC2 instance

sudo apt update -y
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
echo "Nginx installed and running!"
