# Allow github actions to write to S3 without needing long-lived
# access keys. This lets github actions deploy the site while keeping
# it secure.

resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

data "aws_iam_policy_document" "github_actions_assume_role" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:beneggers.com/*"]
    }
  }
}

resource "aws_iam_role" "github_actions" {
  name               = "github-actions"
  assume_role_policy = data.aws_iam_policy_document.github_actions_assume_role.json
}

resource "aws_s3_bucket_policy" "github_actions" {
  bucket = aws_s3_bucket.main.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          "AWS" : aws_iam_role.github_actions.arn
        }
        Action = [
          "s3:DeleteObject",
          "s3:PutObject",
          "s3:GetObject"
        ],
        Resource = "${aws_s3_bucket.main.arn}/*",
        Condition = {
          StringEquals = {
            "aws:userid" = aws_iam_role.github_actions.arn
          }
        }
      },
      {
        Effect = "Allow",
        Principal = {
          "AWS" : aws_iam_role.github_actions.arn
        }
        Action = [
          "s3:ListBucket"
        ],
        Resource = "${aws_s3_bucket.main.arn}",
        Condition = {
          StringEquals = {
            "aws:userid" = aws_iam_role.github_actions.arn
          }
        }
      }
    ]
  })
}
