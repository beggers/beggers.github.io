resource "aws_s3_bucket" "main" {
  bucket = var.bucketName
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
    suffix = "index.html"
  }
  error_document {
    key = "../index.html"
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
    bucket = aws_s3_bucket.main.id
    acl    = "public-read"
    depends_on = [aws_s3_bucket_ownership_controls.main]
}

resource "aws_s3_bucket_policy" "main" {
  bucket = aws_s3_bucket.main.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Principal = "*"
        Action = [
          "s3:*",
        ]
        Effect = "Allow"
        Resource = [
          "arn:aws:s3:::${var.bucketName}",
          "arn:aws:s3:::${var.bucketName}/*"
        ]
      },
      {
        Sid = "PublicReadGetObject"
        Principal = "*"
        Action = [
          "s3:GetObject",
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:s3:::${var.bucketName}",
          "arn:aws:s3:::${var.bucketName}/*"
        ]
      },
    ]
  })
  depends_on = [aws_s3_bucket_public_access_block.main]
}

resource "aws_s3_object" "index" {
  bucket        = aws_s3_bucket.main.id
  key           = "index.html"
  source        = "../index.html"
  etag          = filemd5("../index.html")
  content_type  = "text/html"
}

resource "aws_s3_object" "favicon" {
  bucket       = aws_s3_bucket.main.id
  key          = "favicon.ico"
  source       = "../favicon.ico"
  etag         = filemd5("../favicon.ico")
  content_type = "image/x-icon"
}
