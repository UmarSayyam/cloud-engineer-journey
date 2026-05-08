output "instance_public_ip" {
    description = "output of public ip of instance"
    value       = aws_instance.my_server.public_ip
}

output "bucket_name" {
    description = "output of s3 bucket name"
    value       = aws_s3_bucket.my_bucket.bucket
}