
# data "aws_iam_policy_document" "s3_code_bucket_document" {
#     statement {
#         actions = ["s3:GetObject"]

#         resources = [
#             "${aws_s3_bucket.code_bucket.arn}/*"
#         ]
#     }
# }

# resource "aws_iam_role" "" {

# }



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

        actions = ["S3:PutObject"]

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
            "logs:CreateLogGroup",
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