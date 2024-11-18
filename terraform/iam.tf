## Policy document for lambda assume role permission (a way of portraying the JSON)
data "aws_iam_policy_document" "assume_role_policy" {
    statement {
        effect = "Allow"

        actions = ["sts:AssumeRole"]

        principals {
            type = "Service"
            identifiers = ["lambda.amazonaws.com"]
        }
    }
}

## iam role for lambda1, for lambda1 to have the lambda assume role permission
resource "aws_iam_role" "role_for_lambda1" {
    name = "role_for_${var.lambda1_name}"
    assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}


## Policy document to PUT an object in the INGESTION S3 bucket (a way of portraying the JSON)
data "aws_iam_policy_document" "s3_put_object_document" {
    statement {
        effect = "Allow"

        actions = ["S3:PutObject", "S3:GetObject"]

        resources = ["${aws_s3_bucket.ingestion_bucket.arn}/*"]
    }
}

## Policy for lambda1, for lambda1 to have the S3 PUT object permission
resource "aws_iam_policy" "s3_put_policy_for_lambda1" {
    name = "s3_put_policy_for_${var.lambda1_name}"
    policy = data.aws_iam_policy_document.s3_put_object_document.json
}

## Attach the S3 PUT object policy to the lambda1 iam role
resource "aws_iam_role_policy_attachment" "s3_put_object_attachment_for_lambda1" {
    role = aws_iam_role.role_for_lambda1.name
    policy_arn = aws_iam_policy.s3_put_policy_for_lambda1.arn
}


## Policy document to log to Cloudwatch
data "aws_iam_policy_document" "Cloudwatch_log_document" {
    statement {
        
        effect = "Allow"

        actions = [
            # "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
            ]

        resources = ["arn:aws:logs:*:*:*"] # Is this ok?
    }
}

## Policy for lambda1, for lambda1 to log to Cloudwatch
resource "aws_iam_policy" "Cloudwatch_log_policy_for_lambda1" {
    name = "Cloudwatch_log_policy_for_lambda1"
    policy = data.aws_iam_policy_document.Cloudwatch_log_document.json
}

## Attach the Cloudwatch log policy to the lambda1 iam role
resource "aws_iam_role_policy_attachment" "Cloudwatch_log_attachment_for_lambda1" {
    role = aws_iam_role.role_for_lambda1.name
    policy_arn = aws_iam_policy.Cloudwatch_log_policy_for_lambda1.arn
}


## iam policy for sns and attach to lambda1 iam role
resource "aws_iam_role_policy" "role_policy_for_lambda1_sns" {
  name = "role_policy_for_lambda1_sns"
  role = aws_iam_role.role_for_lambda1.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sns:Publish",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action = [
          "logs:StartQuery",
          "logs:GetQueryResults",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action = [
          "iam:ListAccountAliases",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

## Policy document for Secrets Manager get secret value permission (a way of portraying the JSON)
data "aws_iam_policy_document" "get_secret_value_policy" {
    statement {
        effect = "Allow"

        actions = ["secretsmanager:GetSecretValue"]

        resources = [ "arn:aws:secretsmanager:eu-west-2:796973515606:secret:totesys-conn-430tOE" ]
    }
}

## Policy for lambda1, for lambda1 to get secret value
resource "aws_iam_policy" "get_secret_value_policy_for_lambda1" {
    name = "get_secret_value_policy_for_${var.lambda1_name}"
    policy = data.aws_iam_policy_document.get_secret_value_policy.json
}

## Attach the get secret value policy to the lambda1 iam role
resource "aws_iam_role_policy_attachment" "get_secret_value_attachment_for_lambda1" {
    role = aws_iam_role.role_for_lambda1.name
    policy_arn = aws_iam_policy.get_secret_value_policy_for_lambda1.arn
}