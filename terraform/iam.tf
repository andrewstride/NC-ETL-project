resource "aws_iam_role" "" {

}

resource "aws_iam_policy_document" "s3_code_bucket_document" {
    statement {
        actions = ["s3:GetObject"]

        resources = [
            "${aws_s3_bucket.code_bucket.arn}/*"
        ]
    }
}

resource "aws_iam_policy_document" "s3_code_bucket_document" {
    statement {
        actions = ["s3:GetObject"]

        resources = [
            "${aws_s3_bucket.code_bucket.arn}/*"
        ]
    }
}