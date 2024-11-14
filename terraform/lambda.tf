## Create adjusted file structure for remote deployment of Lambda
resource "null_resource" "create_lambda1_file_structure" {
    provisioner "local-exec" {
        command = "rm -f ../terraform-remote-deployment/*.zip && mkdir -p ${path.module}/${var.lambda1_deployment_dir} && cp -rv ${path.module}/${var.lambda1_source_dir} ${path.module}/${var.lambda1_deployment_dir}"
    }
    triggers = {
        dependencies = filemd5("${path.module}/../src/week1_lambda.py")
        dependencies = filemd5("${path.module}/../src/connection.py")
        dependencies = filemd5("${path.module}/../src/utils.py")
    }
}

## prevent archive_file taking place before "create_lambda1_file_structure occurs"
data "null_data_source" "wait_for_create_lambda1_file_structure" {
  inputs = {
    create_lambda1_file_structure_id = "${null_resource.create_lambda1_file_structure.id}"
    source_dir = "${path.module}/${var.lambda1_deployment_dir}"
  }
}
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
    layers = [aws_lambda_layer_version.layer_for_lambda1.arn]
}

## Zip file for lambda1 functions - getting the python lambda1 functions from the folder where they are stored, and zipping it.
data "archive_file" "lambda1_handler_func" {
    type = "zip"
    source_dir = var.lambda1_deployment_dir
    output_path = "${path.module}/../terraform-remote-deployment/${var.lambda1_name}.zip"
}