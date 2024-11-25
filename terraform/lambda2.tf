## Create lambda2
resource "aws_lambda_function" "lambda2" {
    function_name = "${var.lambda2_name}"
    s3_bucket = aws_s3_bucket.code_bucket.bucket
    s3_key = "lambda2/${var.lambda2_name}.zip"
    role = aws_iam_role.role_for_lambda2.arn
    handler = "src/week2_lambda.lambda_handler"

    timeout = 180
    source_code_hash = data.archive_file.lambda2_handler_func.output_base64sha256 # check for code updates
    runtime = "python3.12"
    layers = ["arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python312:14", 
                aws_lambda_layer_version.layer_for_lambda2.arn, 
                aws_lambda_layer_version.overwrite_awslayer.arn ]
    depends_on = [aws_cloudwatch_log_group.log_group_for_lambda2]
}

## Zip file for lambda2 functions - getting the python lambda2 functions from the folder where they are stored, and zipping it.
data "archive_file" "lambda2_handler_func" {
    type = "zip"
    source_dir = var.lambda2_source_dir
    excludes = var.lambda_comp_exclude_list
    output_path = "${path.module}/../terraform-remote-deployment/${var.lambda2_name}.zip"
}