## zip file for lambda2 in S3 code bucket
resource "aws_s3_object" "lambda2" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "${var.lambda2_name}/${var.lambda2_name}.zip"
  source = data.archive_file.lambda2_handler_func.output_path
  etag   = filemd5(data.archive_file.lambda2_handler_func.output_path)
  depends_on = [ data.archive_file.lambda2_handler_func ]
}

## zip file for lambda2 layer in S3 code bucket
resource "aws_s3_object" "lambda2_layer" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "${var.lambda2_name}_layer/layer.zip"
  source = data.archive_file.layer_code_for_lambda2.output_path
  etag   = filemd5(data.archive_file.layer_code_for_lambda2.output_path)
  depends_on = [ data.archive_file.layer_code_for_lambda2 ]
}

