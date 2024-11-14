## sns topic for lambda1
resource "aws_sns_topic" "alert_for_lambda1" {
    name = "alert_for_lambda1"
}

## sns topic subscription for lambda1 - links to email account
resource "aws_sns_topic_subscription" "email_subscription_for_lambda1" {
    topic_arn = aws_sns_topic.alert_for_lambda1.arn
    protocol = "email"
    endpoint = "TheTerraformers@protonmail.com"
}

# resource "aws_lambda_function_event_invoke_config" "error_notification_for_lambda1_when_run_fails" {
#     function_name = aws_lambda_function.lambda1.function_name
#     qualifier = "$LATEST"

#     destination_config {
#       on_failure {
#         destination = aws_sns_topic.alert_for_lambda1.arn
#       }
#     }
# }