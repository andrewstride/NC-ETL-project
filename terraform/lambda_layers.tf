## pip install requirements for lambda1 (from requirements-lambda1.txt file)
resource "null_resource" "create_dependencies" {
    provisioner "local-exec" {
        command = "pip install -r ${path.module}/../requirements-${var.lambda1_name}.txt -t ${path.module}/${var.lambda1_layer_deployment_dir}/python"
    }
    triggers = {
        source_code_hash = "${filebase64sha256("${path.module}/../requirements-${var.lambda1_name}.txt")}"
        # dependencies = filemd5("${path.module}/../requirements-${var.lambda1_name}.txt")
    }
}

## zip file for lambda1 layer - getting the dependecies file locally and zipping it
data "archive_file" "layer_code_for_lambda1" {
    type = "zip"

    output_path = "${path.module}/../terraform-remote-deployment/lambda1_layer.zip"
    source_dir = "${path.module}/${var.lambda1_layer_deployment_dir}"
    depends_on = [null_resource.create_dependencies]
}

## Create lambda1 layer from the zip file
resource "aws_lambda_layer_version" "layer_for_lambda1" {
    layer_name = "layer_for_${var.lambda1_name}"
    s3_bucket = aws_s3_object.lambda1_layer.bucket
    s3_key = aws_s3_object.lambda1_layer.key
}