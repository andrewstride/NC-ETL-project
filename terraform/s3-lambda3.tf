## zip file for lambda3 in S3 code bucket
resource "aws_s3_object" "lambda3" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "${var.lambda3_name}/${var.lambda3_name}.zip"
  source = data.archive_file.lambda3_handler_func.output_path
  etag   = filemd5(data.archive_file.lambda3_handler_func.output_path)
  depends_on = [ data.archive_file.lambda3_handler_func ]
}

## zip file for lambda3 layer in S3 code bucket
resource "aws_s3_object" "lambda3_layer" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "${var.lambda3_name}_layer/layer.zip"
  source = data.archive_file.layer_code_for_lambda3.output_path
  etag   = filemd5(data.archive_file.layer_code_for_lambda3.output_path)
  depends_on = [ data.archive_file.layer_code_for_lambda3 ]
}