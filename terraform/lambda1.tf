## Create lambda1
resource "aws_lambda_function" "lambda1" {
    function_name = "${var.lambda1_name}"
    s3_bucket = aws_s3_bucket.code_bucket.bucket
    s3_key = "lambda1/${var.lambda1_name}.zip"
    role = aws_iam_role.role_for_lambda1.arn
    handler = "src/week1_lambda.lambda_handler"

    timeout = 180
    source_code_hash = data.archive_file.lambda1_handler_func.output_base64sha256 # check for code updates
    runtime = "python3.12"
    layers = ["arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python312:14", 
                aws_lambda_layer_version.layer_for_lambda1.arn,
                aws_lambda_layer_version.overwrite_awslayer.arn ] # ORDER MATTERS
    depends_on = [aws_cloudwatch_log_group.log_group_for_lambda1]
}

## Zip file for lambda1 functions - getting the python lambda1 functions from the folder where they are stored, and zipping it.
data "archive_file" "lambda1_handler_func" {
    type = "zip"
    source_dir = var.lambda1_source_dir
    excludes = var.lambda_comp_exclude_list
    output_path = "${path.module}/../terraform-remote-deployment/${var.lambda1_name}.zip"
}



