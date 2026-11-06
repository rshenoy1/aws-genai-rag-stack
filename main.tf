
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "enterprise_data_lake" {
  bucket        = "acme-corp-enterprise-genai-data-lake"
  force_destroy = true
}

resource "aws_sqs_queue" "traffic_queue" {
  name                        = "enterprise-genai-traffic-queue.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "enterprise-genai-lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "://amazonaws.com" }
    }]
  })
}

resource "aws_iam_policy" "lambda_least_privilege_policy" {
  name = "lambda-least-privilege-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          "arn:aws:s3:::acme-corp-enterprise-genai-data-lake",
          "arn:aws:s3:::acme-corp-enterprise-genai-data-lake/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["bedrock:InvokeModel"]
        Resource = [
          "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-v2:0",
          "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_privileges" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_least_privilege_policy.arn
}

