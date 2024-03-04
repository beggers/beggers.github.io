resource "aws_cloudfront_origin_access_identity" "main" {}

resource "aws_cloudfront_distribution" "main" {
  origin {
    domain_name = aws_s3_bucket.main.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.main.bucket}"
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.main.cloudfront_access_identity_path
    }
  }

  default_root_object = "index.html"
  enabled             = true
  is_ipv6_enabled     = true
  aliases             = ["beneggers.com", "www.beneggers.com"]

  # If there is a 404, return index.html with a HTTP 200 Response
  custom_error_response {
    error_caching_min_ttl = 3000
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.main.bucket}"

    forwarded_values {
      query_string = true
      cookies {
        forward = "none"
      }
    }
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  price_class = "PriceClass_100"
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.main.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}

data "aws_iam_policy_document" "invalidate_cloudfront_cache" {
  statement {
    actions = [
      "cloudfront:CreateInvalidation",
    ]
    effect = "Allow"
    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values = [
        aws_iam_role.github_actions.arn
      ]
    }
    resources = [
      aws_cloudfront_distribution.main.arn
    ]
  }
}

resource "aws_iam_policy" "invalidate_cloudfront_cache" {
  name        = "invalidate_cloudfront_cache"
  description = "Invalidate CloudFront Cache"
  policy      = data.aws_iam_policy_document.invalidate_cloudfront_cache.json
}
