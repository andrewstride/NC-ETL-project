## CloudWatch log group for lambda1
resource "aws_cloudwatch_log_group" "log_group_for_lambda1" {
    name = "/aws/lambda/${var.lambda1_name}_log_group"

    retention_in_days = 0 # never expires

    tags = {
        name = "log_group_for_${var.lambda1_name}"
        environment = "dev"
        description = "A Cloudwatch log group for lambda1 to send logs to."
    }
}

## CloudWatch metric filter for lambda 1
resource "aws_cloudwatch_log_metric_filter" "log_error_count_metric_for_lambda1" {
    name = "log_errors_count_metric_for_${var.lambda1_name}"
    pattern = "ERROR"
    log_group_name = aws_cloudwatch_log_group.log_group_for_lambda1.name
    
    metric_transformation {
       name = "${var.lambda1_name} error count"
       namespace = "${var.lambda1_name} errors"
       value = 1
    }
}

## CloudWatch metric alarm for lambda1
resource "aws_cloudwatch_metric_alarm" "error_count_alarm_for_lambda1" {
    alarm_name = "error_count_alarm_for_${var.lambda1_name}"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods = 1
    metric_name = aws_cloudwatch_log_metric_filter.log_error_count_metric_for_lambda1.name
    namespace = "${var.lambda1_name} errors"
    period = 1800
    statistic = "SampleCount"
    threshold = 0
    alarm_description = "${var.lambda1_name} has an error!!!"
    insufficient_data_actions = []
    alarm_actions = [aws_sns_topic.alert_for_lambda1.arn]
}