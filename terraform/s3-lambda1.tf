## zip file for lambda1 in S3 code bucket
resource "aws_s3_object" "lambda1" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "${var.lambda1_name}/${var.lambda1_name}.zip"
  source = data.archive_file.lambda1_handler_func.output_path
  etag   = filemd5(data.archive_file.lambda1_handler_func.output_path)
  depends_on = [ data.archive_file.lambda1_handler_func ]
}

## zip file for lambda1 layer in S3 code bucket
resource "aws_s3_object" "lambda1_layer" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "${var.lambda1_name}_layer/layer.zip"
  source = data.archive_file.layer_code_for_lambda1.output_path
  etag   = filemd5(data.archive_file.layer_code_for_lambda1.output_path)
  depends_on = [ data.archive_file.layer_code_for_lambda1 ]
}
