data "aws_iam_policy_document" "website_policy" {
  statement {
    principals {
      type = "AWS"
      identifiers = [
        aws_cloudfront_origin_access_identity.main.iam_arn
      ]
    }
    actions = [
      "s3:Get*",
      "s3:List*",
      "s3:Put*",
      "s3:DeleteObject"
    ]
    effect = "Allow"
    resources = [
      "arn:aws:s3:::beneggers.com",
      "arn:aws:s3:::beneggers.com/*"
    ]
  }
  statement {
    actions = [
      "s3:*",
    ]
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        aws_iam_role.github_actions.arn
      ]
    }
    resources = [
      "${aws_s3_bucket.main.arn}/*",
      "${aws_s3_bucket.main.arn}"
    ]
  }
}
