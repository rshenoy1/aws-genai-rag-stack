provider "aws" {
  region = "us-east-1"
}

# ========================================================
# 1. IAM SECURITY ROLES: LEAST-PRIVILEGE COMPUTATION ACCESS
# ========================================================
resource "aws_iam_role" "squad_lambda_exec_role" {
  name = "enterprise-multi-agent-lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "://amazonaws.com" }
    }]
  })
}

resource "aws_iam_role" "step_functions_orchestrator_role" {
  name = "enterprise-step-functions-squad-orchestrator-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "://amazonaws.com" }
    }]
  })
}

resource "aws_iam_policy" "squad_least_privilege_policy" {
  name        = "multi-agent-squad-least-privilege-policy"
  description = "Enforces isolated resource access controls across worker agents and orchestration pipelines."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["lambda:InvokeFunction"]
        Resource = ["*"]
      },
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = [
          "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-v2:0",
          "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = ["arn:aws:logs:*:*:*"]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_lambda_privileges" {
  role       = aws_iam_role.squad_lambda_exec_role.name
  policy_arn = aws_iam_policy.squad_least_privilege_policy.arn
}

resource "aws_iam_role_policy_attachment" "attach_sfn_privileges" {
  role       = aws_iam_role.step_functions_orchestrator_role.name
  policy_arn = aws_iam_policy.squad_least_privilege_policy.arn
}

# ========================================================
# 2. SEVERLESS COMPUTE LAYERS (ISOLATED LAMBDA MICROSERVICES)
# ========================================================
resource "aws_lambda_function" "production_researcher" {
  filename      = "lambda_workers.zip"
  function_name = "enterprise-worker-researcher"
  role          = aws_iam_role.squad_lambda_exec_role.arn
  handler       = "lambda_workers.lambda_handler_researcher"
  runtime       = "python3.12"
}

resource "aws_lambda_function" "production_analyst" {
  filename      = "lambda_workers.zip"
  function_name = "enterprise-worker-analyst"
  role          = aws_iam_role.squad_lambda_exec_role.arn
  handler       = "lambda_workers.lambda_handler_analyst"
  runtime       = "python3.12"
}

resource "aws_lambda_function" "production_writer" {
  filename      = "lambda_workers.zip"
  function_name = "enterprise-worker-writer"
  role          = aws_iam_role.squad_lambda_exec_role.arn
  handler       = "lambda_workers.lambda_handler_writer"
  runtime       = "python3.12"
}

# ========================================================
# 3. AWS STEP FUNCTIONS: PARALLEL STATE MACHINE ENGINE
# ========================================================
resource "aws_sfn_state_machine" "multi_agent_squad_orchestrator" {
  name     = "enterprise-multi-agent-squad-orchestrator"
  role_arn = aws_iam_role.step_functions_orchestrator_role.arn

  definition = jsonencode({
    Comment = "Enterprise High-Performance Parallel Multi-Agent Collaboration Orchestrator State Machine"
    StartAt = "ParallelAgentExecution"
    States = {
      ParallelAgentExecution = {
        Type       = "Parallel"
        Next       = "InvokeWriterAgent"
        ResultPath = "$.Result.CombinedSquadOutputs"
        Branches = [
          {
            StartAt = "InvokeParallelResearcher"
            States = {
              InvokeParallelResearcher = {
                Type     = "Task"
                Resource = "${aws_lambda_function.production_researcher.arn}"
                End      = true
              }
            }
          },
          {
            StartAt = "InvokeParallelAnalyst"
            States = {
              InvokeParallelAnalyst = {
                Type     = "Task"
                Resource = "${aws_lambda_function.production_analyst.arn}"
                End      = true
              }
            }
          }
        ]
      }
      InvokeWriterAgent = {
        Type     = "Task"
        Resource = "${aws_lambda_function.production_writer.arn}"
        End      = true
      }
    }
  })
}
