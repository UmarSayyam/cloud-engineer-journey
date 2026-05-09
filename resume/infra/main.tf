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

resource "aws_s3_bucket" "resume" {
  bucket = "umar-cloud-resume-2026"

  tags = {
    Name    = "umar-cloud-resume"
    Project = "cloud-resume-challenge"
  }
}

resource "aws_s3_bucket_website_configuration" "resume" {
  bucket = aws_s3_bucket.resume.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "resume" {
  bucket = aws_s3_bucket.resume.id

  block_public_acls         = false
  block_public_policy       = false
  ignore_public_acls        = false
  restrict_public_buckets   = false
}

resource "aws_s3_bucket_policy" "resume" {
  bucket = aws_s3_bucket.resume.id
  depends_on = [aws_s3_bucket_public_access_block.resume]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
        Sid         = "PublicReadGetObject"
        Effect      = "Allow"
        Principal   = "*"
        Action      = "s3:GetObject"
        Resource    = "${aws_s3_bucket.resume.arn}/*"
    }]
  })
}

resource "aws_cloudfront_distribution" "resume" {
  origin {
    domain_name = aws_s3_bucket_website_configuration.resume.website_endpoint
    origin_id = "S3-resume"

    custom_origin_config {
      http_port = 80
      https_port = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols = ["TLSv1.2"]
    }
  }

  enabled = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods = [ "GET", "HEAD" ]
    cached_methods = ["GET", "HEAD"]
    target_origin_id = "S3-resume"
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Name = "umar-resume-cdn"
    Project = "cloud-resume-challenge"
  }
}

output "cloudfront_url" {
  value = "https://${aws_cloudfront_distribution.resume.domain_name}"
}