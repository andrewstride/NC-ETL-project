## zip file for lambda3 layer - getting the dependencies file locally and zipping it
data "archive_file" "layer_code_for_lambda3" {
    type = "zip"
    output_path = "${path.module}/../terraform-remote-deployment/lambda3_layer.zip"
    source_dir = "${path.module}/${var.lambda3_layer_deployment_dir}"

}

## Create lambda3 layer from the zip file
resource "aws_lambda_layer_version" "layer_for_lambda3" {
    layer_name = "layer_for_${var.lambda3_name}"
    s3_bucket = aws_s3_object.lambda3_layer.bucket
    s3_key = aws_s3_object.lambda3_layer.key
}