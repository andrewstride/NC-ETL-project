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

## Policy document for Secrets Manager get secret value permission (a way of portraying the JSON)
data "aws_iam_policy_document" "get_secret_value_policy" {
    statement {
        effect = "Allow"
        actions = ["secretsmanager:GetSecretValue"]
        resources = [ "arn:aws:secretsmanager:eu-west-2:796973515606:secret:totesys-conn-430tOE" ]
    }
}
