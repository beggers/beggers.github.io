resource "aws_s3_bucket" "terraform_state" {
  // Only hyphens are allowed in bucket names
  bucket = "beneggers-terraform-state"
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.bucket
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "beneggers-terraform-state"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

data "aws_iam_policy_document" "github_actions_policy" {
  statement {
    actions = [
      "s3:DeleteObject",
      "s3:PutObject",
      "s3:GetObject"
    ]
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        aws_iam_role.github_actions.arn
      ]
    }
    resources = [
      "${aws_s3_bucket.terraform_state.arn}/*"
    ]
  }
  statement {
    actions = [
      "s3:ListBucket"
    ]
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        aws_iam_role.github_actions.arn
      ]
    }
    resources = [
      "${aws_s3_bucket.terraform_state.arn}"
    ]
  }
}

resource "aws_s3_bucket_policy" "terraform_state" {
  bucket     = aws_s3_bucket.terraform_state.id
  policy     = data.aws_iam_policy_document.github_actions_policy.json
  depends_on = [aws_s3_bucket_public_access_block.terraform_state]
}
