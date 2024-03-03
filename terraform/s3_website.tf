resource "aws_s3_bucket" "main" {
  bucket = "beneggers.com"
  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_s3_bucket" "www" {
  bucket = "www.beneggers.com"
}

resource "aws_s3_bucket_public_access_block" "main" {
  bucket = aws_s3_bucket.main.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_public_access_block" "www" {
  bucket = aws_s3_bucket.www.id

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
    key = "../src/index.html"
  }
}

resource "aws_s3_bucket_website_configuration" "www" {
  bucket = aws_s3_bucket.www.id
  redirect_all_requests_to {
    host_name = aws_s3_bucket.main.bucket_regional_domain_name
    protocol  = "https"
  }
}

resource "aws_s3_bucket_ownership_controls" "main" {
  bucket = aws_s3_bucket.main.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
  depends_on = [aws_s3_bucket_public_access_block.main]
}

resource "aws_s3_bucket_ownership_controls" "www" {
  bucket = aws_s3_bucket.www.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
  depends_on = [aws_s3_bucket_public_access_block.www]
}

resource "aws_s3_bucket_acl" "main" {
  bucket     = aws_s3_bucket.main.id
  acl        = "private"
  depends_on = [aws_s3_bucket_ownership_controls.main]
}

resource "aws_s3_bucket_acl" "www" {
  bucket     = aws_s3_bucket.www.id
  acl        = "private"
  depends_on = [aws_s3_bucket_ownership_controls.www]
}

resource "aws_s3_bucket_policy" "main" {
  bucket     = aws_s3_bucket.main.id
  policy     = data.aws_iam_policy_document.website_policy.json
  depends_on = [aws_s3_bucket_public_access_block.main]
}

resource "aws_s3_object" "index" {
  bucket       = aws_s3_bucket.main.id
  key          = "index.html"
  source       = "../src/index.html"
  etag         = filemd5("../src/index.html")
  content_type = "text/html"
}

resource "aws_s3_object" "favicon" {
  bucket       = aws_s3_bucket.main.id
  key          = "favicon.ico"
  source       = "../static/favicon.ico"
  etag         = filemd5("../static/favicon.ico")
  content_type = "image/x-icon"
}

resource "aws_s3_object" "style" {
  bucket       = aws_s3_bucket.main.id
  key          = "style.css"
  source       = "../src/style.css"
  etag         = filemd5("../src/style.css")
  content_type = "text/css"
}

resource "aws_s3_object" "script" {
  bucket       = aws_s3_bucket.main.id
  key          = "script.js"
  source       = "../src/script.js"
  etag         = filemd5("../src/script.js")
  content_type = "text/javascript"
}
