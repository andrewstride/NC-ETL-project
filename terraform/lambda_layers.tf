## pip install requirements for lambda1 (from requirements-lambda1.txt file)
resource "null_resource" "create_dependencies" {
    provisioner "local-exec" {
        command = "pip install -r ${path.module}/../requirements-${var.lambda1_name}.txt -t ${path.module}/${var.lambda1_layer_deployment_dir}/python"
    }
    triggers = {
        dependencies = filemd5("${path.module}/../requirements-${var.lambda1_name}.txt")
    }
}

## prevent archive_file taking place before "create_dependencies occurs"
data "null_data_source" "wait_for_create_dependencies" {
  inputs = {
    create_dependencies_id = "${null_resource.create_dependencies.id}"
    source_dir = "${path.module}/${var.lambda1_layer_deployment_dir}"
  }
}
## zip file for lambda1 layer - getting the dependecies file locally and zipping it
data "archive_file" "layer_code_for_lambda1" {
    type = "zip"
    output_path = "${path.module}/../terraform-remote-deployment/lambda1_layer.zip"
    source_dir  = "${data.null_data_source.wait_for_create_dependencies.outputs["source_dir"]}"
    #source_dir = "${path.module}/${var.lambda1_layer_deployment_dir}"
}

## Create lambda1 layer from the zip file
resource "aws_lambda_layer_version" "layer_for_lambda1" {
    layer_name = "layer_for_${var.lambda1_name}"
    s3_bucket = aws_s3_object.lambda1_layer.bucket
    s3_key = aws_s3_object.lambda1_layer.key
}