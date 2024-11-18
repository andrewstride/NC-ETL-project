## sns topic for lambdas
resource "aws_sns_topic" "alert_for_lambda" {
    name = "alert_for_lambda"
}

## sns topic subscription for lambdas - links to email account
resource "aws_sns_topic_subscription" "email_subscription_for_lambda" {
    topic_arn = aws_sns_topic.alert_for_lambda.arn
    protocol = "email"
    endpoint = "TheTerraformers@protonmail.com"
}

