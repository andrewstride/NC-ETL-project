resource "aws_lambda_function" "lambda1" {
    function_name = "${var.lambda1_name}"
    s3_bucket = aws_s3_bucket.code_bucket.bucket
    s3_key = "lambda1/${var.lambda1_name}.zip"
    role = aws_iam_role.lambda1_role.arn
    handler = "lambda1.lambda_handler"
    runtime = "python3.12"
}

data "archive_file" "lambda1" {
    type = "zip"
    source_file = var.lambda1_source_file
    output_path = "${path.module}/../${var.lambda1_name}.zip"
}

resource "aws_lambda_permission" "allow_s3" {
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda1.function_name
  principal = "s3.amazonaws.com"
  source_arn = aws_s3_bucket.ingestion_bucket.arn
  source_account = data.aws_caller_identity.current.account_id
}