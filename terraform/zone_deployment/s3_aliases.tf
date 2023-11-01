// S3 website config for aliases is different: it involves a redirect rather
// than directly serving the resource. Rather than create some main and alias
// resources separately (due to difference) and some of them together, we
// just keep them completely separate.

resource "aws_s3_bucket" "aliases" {
  for_each = toset(var.domain_aliases)

  bucket = each.value
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_public_access_block" "aliases" {
  for_each = aws_s3_bucket.aliases

  bucket = each.value.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_website_configuration" "aliases" {
  for_each = aws_s3_bucket.aliases

  bucket = each.value.id

  redirect_all_requests_to {
    host_name = aws_s3_bucket.main.bucket_regional_domain_name
    protocol  = "https"
  }
}

resource "aws_s3_bucket_ownership_controls" "aliases" {
  for_each = aws_s3_bucket.aliases

  bucket = each.value.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
  depends_on = [aws_s3_bucket_public_access_block.main]
}

resource "aws_s3_bucket_acl" "aliases" {
  for_each = aws_s3_bucket.aliases

  bucket = each.value.id

  acl        = "private"
  depends_on = [aws_s3_bucket_ownership_controls.aliases]
}
