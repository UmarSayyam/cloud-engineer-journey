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

# S3 buckets for file uploads
resource "aws_s3_bucket" "pipeline_bucket" {
  bucket = "umar-serverless-pipeline-2026"

  tags = {
    Project = "serverless-pipeline"
  }
}

# DynamoDb for Analysis results
resource "aws_dynamodb_table" "file_analysis" {
  name = "file-analysis"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "file_key"

  attribute {
    name = "file_key"
    type = "S"
  }

  tags = {
    Project = "serverless-pipeline"
  }
}

# IAM role for lambda
resource "aws_iam_role" "pipeline_lambda_role" {
  name = "pipeline-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = { Service = "lambda.amazonaws.com"}
    }]
  })
}

# IAM policy
resource "aws_iam_role_policy" "pipeline_lambda_policy" {
  name = "pipeline-lambda-policy"
  role = aws_iam_role.pipeline_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            Effect = "Allow"
            Action = ["s3:GetObject"]
            Resource = "${aws_s3_bucket.pipeline_bucket.arn}/*"
        },
        {
            Effect = "Allow"
            Action = ["dynamodb:PutItem", "dynamodb:GetItem"]
            Resource = aws_dynamodb_table.file_analysis.arn
        },
        {
            Effect = "Allow"
            Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
            Resource = "arn:aws:logs:*:*:*"
        }
    ]
  })
}

# Zip Lambda
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_function.py"
  output_path = "${path.module}/lambda_function.zip"
}

# Lambda function
resource "aws_lambda_function" "pipeline" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "serverless-file-pipeline"
  role             = aws_iam_role.pipeline_lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  tags = {
    Project = "serverless-pipeline"
  }
}

# Allow S3 to invoke Lambda
resource "aws_lambda_permission" "s3_trigger" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pipeline.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.pipeline_bucket.arn
}

# S3 event notification to trigger Lambda
resource "aws_s3_bucket_notification" "pipeline_trigger" {
  bucket = aws_s3_bucket.pipeline_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.pipeline.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".txt"
  }

  depends_on = [aws_lambda_permission.s3_trigger]
}

output "bucket_name" {
  value = aws_s3_bucket.pipeline_bucket.bucket
}

output "function_name" {
  value = aws_lambda_function.pipeline.function_name
}