## CloudWatch log group for lambda1
resource "aws_cloudwatch_log_group" "log_group_for_lambda1" {
    name                = "/aws/lambda/${var.lambda1_name}"
    retention_in_days   = 3 # Set to 3 days to demonstrate functionality during project duration
    tags                = {
        name            = "${var.lambda1_name} log group"
        environment     = "dev"
        description     = "A Cloudwatch log group for lambda1 to send logs to."
    }
}

## CloudWatch metric filter for lambda1
resource "aws_cloudwatch_log_metric_filter" "log_error_count_metric_for_lambda1" {
    name            = "${var.lambda1_name}_error"
    pattern         = "ERROR"
    log_group_name  = aws_cloudwatch_log_group.log_group_for_lambda1.name
    
    metric_transformation {
       name         = "${var.lambda1_name}_error"
       namespace    = "log_errors"
       value        = 1
    }
}

## CloudWatch metric alarm for lambda1
resource "aws_cloudwatch_metric_alarm" "error_count_alarm_for_lambda1" {
    alarm_name                  = "${var.lambda1_name}_error"
    comparison_operator         = "GreaterThanOrEqualToThreshold"
    evaluation_periods          = 1
    metric_name                 = aws_cloudwatch_log_metric_filter.log_error_count_metric_for_lambda1.name
    namespace                   = "log_errors"
    period                      = 300
    statistic                   = "SampleCount"
    threshold                   = 1
    alarm_description           = "${var.lambda1_name} has an error!!!"
    treat_missing_data          = "notBreaching"
    datapoints_to_alarm         = 1
    insufficient_data_actions   = []
    alarm_actions               = [aws_sns_topic.alert_for_lambda.arn]
}