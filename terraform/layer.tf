## Create numpy/fastparquet layer from the zip file
resource "aws_lambda_layer_version" "overwrite_awslayer" {
    layer_name = "overwrite_awslayer"
    s3_bucket = aws_s3_object.overwrite_awslayer.bucket
    s3_key = aws_s3_object.overwrite_awslayer.key
}