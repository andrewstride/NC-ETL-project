## iam role for lambda3, for lambda3 to have the lambda assume role permission
resource "aws_iam_role" "role_for_lambda3" {
    name = "role_for_${var.lambda3_name}"
    assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

## Policy document to GET an object from the PROCESSING S3 bucket
data "aws_iam_policy_document" "s3_get_object_document_lambda3" {
    statement {
        effect = "Allow"
        actions = ["S3:PutObject"]
        resources = ["${aws_s3_bucket.processing_bucket.arn}/*"]
    }
}

## Policy for lambda3 to have the S3 GET object permission to PROCESSING
resource "aws_iam_policy" "s3_get_policy_for_lambda3" {
    name = "s3_get_policy_for_${var.lambda3_name}"
    policy = data.aws_iam_policy_document.s3_get_object_document_lambda3.json
}

## Attach the S3 GET object policy to the lambda3 iam role
resource "aws_iam_role_policy_attachment" "s3_get_object_attachment_for_lambda3" {
    role = aws_iam_role.role_for_lambda3.name
    policy_arn = aws_iam_policy.s3_get_policy_for_lambda3.arn
}

## Policy for lambda3, for lambda3 to log to Cloudwatch
resource "aws_iam_policy" "Cloudwatch_log_policy_for_lambda3" {
    name = "Cloudwatch_log_policy_for_lambda3"
    policy = data.aws_iam_policy_document.Cloudwatch_log_document.json
}

## Attach the Cloudwatch log policy to the lambda3 iam role
resource "aws_iam_role_policy_attachment" "Cloudwatch_log_attachment_for_lambda3" {
    role = aws_iam_role.role_for_lambda3.name
    policy_arn = aws_iam_policy.Cloudwatch_log_policy_for_lambda3.arn
}

## iam policy for sns and attach to lambda3 iam role
resource "aws_iam_role_policy" "role_policy_for_lambda3_sns" {
  name = "role_policy_for_lambda3_sns"
  role = aws_iam_role.role_for_lambda3.name

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
