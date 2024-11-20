## zip file for lambda1 layer - getting the dependencies file locally and zipping it
data "archive_file" "layer_code_for_lambda1" {
    type = "zip"
    output_path = "${path.module}/../terraform-remote-deployment/lambda1_layer.zip"
    source_dir = "${path.module}/${var.lambda1_layer_deployment_dir}"

}

## Create lambda1 layer from the zip file
resource "aws_lambda_layer_version" "layer_for_lambda1" {
    layer_name = "layer_for_${var.lambda1_name}"
    s3_bucket = aws_s3_object.lambda1_layer.bucket
    s3_key = aws_s3_object.lambda1_layer.key
}



