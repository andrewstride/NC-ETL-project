## iam role for lambda2, for lambda2 to have the lambda assume role permission
resource "aws_iam_role" "role_for_lambda2" {
    name = "role_for_${var.lambda2_name}"
    assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

## Policy document to PUT an object in the PROCESSING S3 bucket (a way of portraying the JSON)
data "aws_iam_policy_document" "s3_put_object_document_lambda2" {
    statement {
        effect = "Allow"
        actions = ["S3:PutObject"]
        resources = ["${aws_s3_bucket.processing_bucket.arn}/*"]
    }
}

## Policy document to GET an object from the INGESTION S3 bucket
data "aws_iam_policy_document" "s3_get_object_document_lambda2" {
    statement {
        effect = "Allow"
        actions = ["S3:GetObject"]
        resources = ["${aws_s3_bucket.ingestion_bucket.arn}/*"]
    }
}

## Policy for lambda2 to have the S3 PUT object permission to PROCESSING
resource "aws_iam_policy" "s3_put_policy_for_lambda2" {
    name = "s3_put_policy_for_${var.lambda2_name}"
    policy = data.aws_iam_policy_document.s3_put_object_document_lambda2.json
}

## Policy for lambda2 to have the S3 GET objection permission from INGESTION
resource "aws_iam_policy" "s3_get_policy_for_lambda2" {
    name = "s3_get_policy_for_${var.lambda2_name}"
    policy = data.aws_iam_policy_document.s3_get_object_document_lambda2.json
}

## Attach the S3 PUT object policy to the lambda2 iam role
resource "aws_iam_role_policy_attachment" "s3_put_object_attachment_for_lambda2" {
    role = aws_iam_role.role_for_lambda2.name
    policy_arn = aws_iam_policy.s3_put_policy_for_lambda2.arn
}

## Attach the S3 GET object from INGESTION policy to the lambda2 iam role
resource "aws_iam_role_policy_attachment" "s3_get_object_attachment_for_lambda2" {
    role = aws_iam_role.role_for_lambda2.name
    policy_arn = aws_iam_policy.s3_get_policy_for_lambda2.arn
}

## Policy for lambda2, for lambda2 to log to Cloudwatch
resource "aws_iam_policy" "Cloudwatch_log_policy_for_lambda2" {
    name = "Cloudwatch_log_policy_for_lambda2"
    policy = data.aws_iam_policy_document.Cloudwatch_log_document.json
}

## Attach the Cloudwatch log policy to the lambda2 iam role
resource "aws_iam_role_policy_attachment" "Cloudwatch_log_attachment_for_lambda2" {
    role = aws_iam_role.role_for_lambda2.name
    policy_arn = aws_iam_policy.Cloudwatch_log_policy_for_lambda2.arn
}


## iam policy for sns and attach to lambda2 iam role
resource "aws_iam_role_policy" "role_policy_for_lambda2_sns" {
  name = "role_policy_for_lambda2_sns"
  role = aws_iam_role.role_for_lambda2.name

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