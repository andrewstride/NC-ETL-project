resource "aws_cloudwatch_log_group" "log_group_for_lambda1" {
    name = "${var.lambda1_name}_log_group"

    retention_in_days = 0 # never expires

    tags = {
        name = "log_group_for_${var.lambda1_name}"
        environment = "dev"
        description = "A Cloudwatch log group for lambda1 to send logs to."
    }
}