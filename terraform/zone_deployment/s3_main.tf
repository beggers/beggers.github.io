resource "aws_s3_bucket" "main" {
  bucket = var.fqdn
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_public_access_block" "main" {
  bucket = aws_s3_bucket.main.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_website_configuration" "main" {
  bucket = aws_s3_bucket.main.id
  index_document {
    suffix = var.file
  }
  error_document {
    key = var.file
  }
}

resource "aws_s3_bucket_ownership_controls" "main" {
  bucket = aws_s3_bucket.main.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
  depends_on = [aws_s3_bucket_public_access_block.main]
}

resource "aws_s3_bucket_acl" "main" {
  bucket     = aws_s3_bucket.main.id
  acl        = "private"
  depends_on = [aws_s3_bucket_ownership_controls.main]
}

resource "aws_s3_bucket_policy" "main" {
  bucket     = aws_s3_bucket.main.id
  policy     = data.aws_iam_policy_document.website_policy.json
  depends_on = [aws_s3_bucket_public_access_block.main]
}

resource "aws_s3_object" "index" {
  bucket       = aws_s3_bucket.main.id
  key          = "index.html"
  source       = "${var.file_directory}${var.file}"
  source_hash  = var.source_hash
  content_type = var.content_type
}
