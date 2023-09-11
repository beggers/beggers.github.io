data "aws_iam_policy_document" "website_policy" {
  statement {
    principals {
      type        = "AWS"
      identifiers = [
        aws_cloudfront_origin_access_identity.main.iam_arn
      ]
    }
    actions = [
      "s3:GetObject",
      "s3:ListBucket"
    ]
    effect = "Allow"
    resources = [
      "arn:aws:s3:::${var.bucketName}",
      "arn:aws:s3:::${var.bucketName}/*"
    ]
  }
}