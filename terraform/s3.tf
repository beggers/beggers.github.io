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

data "aws_iam_policy_document" "website_policy" {
  statement {
    principals {
      type = "AWS"
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
      "arn:aws:s3:::beneggers.com",
      "arn:aws:s3:::beneggers.com/*"
    ]
  }
  # TODO it's awkward to have all the policies in one place -- ought to
  # keep this policy next to the Github Actions role definiton.
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

resource "aws_s3_bucket_policy" "main" {
  bucket     = aws_s3_bucket.main.id
  policy     = data.aws_iam_policy_document.website_policy.json
  depends_on = [aws_s3_bucket_public_access_block.main]
}

module "site_files" {
  source   = "hashicorp/dir/template"
  version  = "1.0.2"
  base_dir = "../dist"
}

resource "aws_s3_object" "site_files" {
  # TODO exclude .js.map
  for_each = module.site_files.files
  bucket   = aws_s3_bucket.main.id

  key          = each.key
  content_type = each.value.content_type

  source  = each.value.source_path
  content = each.value.content

  etag = each.value.digests.md5
}
