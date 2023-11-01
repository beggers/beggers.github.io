data "aws_iam_policy_document" "website_policy" {
  statement {
    principals {
      type = "AWS"
      identifiers = [
        var.cloudfront_access_identity_arn
      ]
    }
    actions = [
      "s3:GetObject",
      "s3:ListBucket"
    ]
    effect = "Allow"
    resources = [
      "arn:aws:s3:::${var.fqdn}",
      "arn:aws:s3:::${var.fqdn}/*"
    ]
  }
}
