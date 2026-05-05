terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

resource "aws_s3_bucket" "my_bucket" {
    bucket = "umar-terraform-bucket-2026"

    tags = {
      Name        =    "umar-terraform-bucket"
      Environment =    "dev"
    }
}

resource "aws_s3_bucket_versioning" "my_bucket_versioning" {
    bucket = aws_s3_bucket.my_bucket.id

    versioning_configuration {
      status = "Enabled"
    }
}


resource "aws_instance" "my_server" {
    ami             = "ami-0388e3ada3d9812da"
    instance_type   = "t3.micro"
    
    tags = {
      Name          = "umar-terraform-server"
      Environment   = "dev" 
    }
}