terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

# DynamoDB table
resource "aws_dynamodb_table" "visitors" {
  name         = "resume-visitors"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "ip"

  attribute {
    name = "ip"
    type = "S"
  }

  tags = {
    Project = "cloud-resume-challenge"
  }
}

# IAM role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "resume-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# IAM policy for Lambda to access DynamoDB and CloudWatch logs
resource "aws_iam_role_policy" "lambda_policy" {
  name = "resume-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:UpdateItem", "dynamodb:Scan"]
        Resource = aws_dynamodb_table.visitors.arn
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Zip the Lambda function
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_function.py"
  output_path = "${path.module}/lambda_function.zip"
}

# Lambda function
resource "aws_lambda_function" "visitor_counter" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "resume-visitor-counter"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  tags = {
    Project = "cloud-resume-challenge"
  }
}

# API Gateway
resource "aws_api_gateway_rest_api" "resume_api" {
  name = "resume-api"
}

resource "aws_api_gateway_resource" "visitors" {
  rest_api_id = aws_api_gateway_rest_api.resume_api.id
  parent_id   = aws_api_gateway_rest_api.resume_api.root_resource_id
  path_part   = "visitors"
}

resource "aws_api_gateway_method" "get_visitors" {
  rest_api_id   = aws_api_gateway_rest_api.resume_api.id
  resource_id   = aws_api_gateway_resource.visitors.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "options_visitors" {
  rest_api_id   = aws_api_gateway_rest_api.resume_api.id
  resource_id   = aws_api_gateway_resource.visitors.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.resume_api.id
  resource_id             = aws_api_gateway_resource.visitors.id
  http_method             = aws_api_gateway_method.get_visitors.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.visitor_counter.invoke_arn
}

resource "aws_api_gateway_integration" "options_integration" {
  rest_api_id = aws_api_gateway_rest_api.resume_api.id
  resource_id = aws_api_gateway_resource.visitors.id
  http_method = aws_api_gateway_method.options_visitors.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "options_200" {
  rest_api_id = aws_api_gateway_rest_api.resume_api.id
  resource_id = aws_api_gateway_resource.visitors.id
  http_method = aws_api_gateway_method.options_visitors.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.resume_api.id
  resource_id = aws_api_gateway_resource.visitors.id
  http_method = aws_api_gateway_method.options_visitors.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [aws_api_gateway_integration.options_integration]
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.visitor_counter.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.resume_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "resume_api" {
  rest_api_id = aws_api_gateway_rest_api.resume_api.id

  depends_on = [
    aws_api_gateway_integration.lambda_integration,
    aws_api_gateway_integration_response.options_integration_response
  ]
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.resume_api.id
  rest_api_id   = aws_api_gateway_rest_api.resume_api.id
  stage_name    = "prod"
}

output "api_url" {
  value = "${aws_api_gateway_stage.prod.invoke_url}/visitors"
}