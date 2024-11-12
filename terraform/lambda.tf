# resource "aws_lambda_function" "lambda1" {
#     function_name = "${var.lambda1_name}"
#     s3_bucket = aws_s3_bucket.code_bucket.bucket
#     s3_key = "lambda1/${var.lambda1_name}.zip"
#     role = aws_iam_role.lambda1_role.arn
#     handler = "lambda1.lambda_handler"
#     runtime = "python3.12"
# }

## Creating the lambda1 function
resource "aws_lambda_function" "lambda1" {
    function_name = "${var.lambda1_name}"
    filename = "${var.lambda1_name}.zip"
    role = aws_iam_role.lambda1_role.arn
    handler = "lambda1.lambda_handler"
    timeout = 180
    source_code_hash = data.archive_file.lambda1_handler_func.output_base64sha256 # check for code updates
    runtime = "python3.12"
}

## Zip file for lambda1 lambda_handler - getting the python lambda_handler function from the file where it is stored, and zipping it.
data "archive_file" "lambda1_handler_func" {
    type = "zip"
    source_file = var.lambda1_source_file
    output_path = "${path.module}/../${var.lambda1_name}.zip"
}



# resource "aws_lambda_permission" "allow_s3" {
#   action = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.lambda1.function_name
#   principal = "s3.amazonaws.com"
#   source_arn = aws_s3_bucket.ingestion_bucket.arn
#   source_account = data.aws_caller_identity.current.account_id
# }