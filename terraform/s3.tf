## S3 bucket to store lambda code
resource "aws_s3_bucket" "code_bucket" {
    bucket = "nc-terraformers-code"
    tags = {
        name = "code_bucket"
        environment = "dev"
        description = "S3 bucket to store and provide lambda_handler code for lambda1."
    }
}

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

## Ingestion S3 bucket
resource "aws_s3_bucket" "ingestion_bucket" {
    bucket = "nc-terraformers-ingestion"
    tags = {
        name = "ingestion_bucket"
        environment = "dev"
        description = "S3 bucket to store extracted raw tables from ToteSys."
    }
}

## Processing S3 bucket
resource "aws_s3_bucket" "processing_bucket" {
    bucket = "nc-terraformers-processing"
    tags = {
        name = "processing_bucket"
        environment = "dev"
        description = "S3 bucket to store processed tables from Lambda2."
    }
}