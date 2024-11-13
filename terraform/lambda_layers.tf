resource "null_resource" "create_dependencies" {
    provisioner "local-exec" {
        command = "pip install -r ${path.module}/../requirements.txt -t ${path.module}/../dependencies/python"
    }
    triggers = {
        dependencies = filemd5("${path.module}/../requirements.txt")
    }
}

data "archive_file" "layer_code_for_lambda1" {
    type = "zip"
    output_path = "${path.module}/../packages/layer/layer.zip"
    source_dir = "${path.module}/../dependencies"
}

resource "aws_lambda_layer_version" "layer_for_lambda1" {
    layer_name = "layer_for_${var.lambda1_name}"
    filename = "${path.module}/../packages/layer/layer.zip"
}