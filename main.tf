resource "aws_s3_bucket" "beneggerscom" {
  bucket = var.bucketName
}

resource "aws_s3_bucket_public_access_block" "beneggerscom_public_access_block" {
  bucket = aws_s3_bucket.beneggerscom.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_website_configuration" "beneggerscom_website_configuration" {
  bucket = aws_s3_bucket.beneggerscom.id
  index_document {
    suffix = "index.html"
  }
  error_document {
    key = "index.html"
  }
}

resource "aws_s3_bucket_ownership_controls" "s3_bucket_acl_ownership" {
  bucket = aws_s3_bucket.beneggerscom.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
  depends_on = [aws_s3_bucket_public_access_block.beneggerscom_public_access_block]
}

resource "aws_s3_bucket_acl" "beneggerscom-acl" {
    bucket = aws_s3_bucket.beneggerscom.id
    acl    = "public-read"
    depends_on = [aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership]
}

resource "aws_s3_bucket_policy" "beneggerscom_bucket_policy" {
  bucket = aws_s3_bucket.beneggerscom.id
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
  depends_on = [aws_s3_bucket_public_access_block.beneggerscom_public_access_block]
}

resource "aws_s3_object" "index" {
  bucket        = aws_s3_bucket.beneggerscom.id
  key           = "index.html"
  source        = "index.html"
  etag          = filemd5("index.html")
  content_type  = "text/html"
}

resource "aws_s3_object" "favicon" {
  bucket       = aws_s3_bucket.beneggerscom.id
  key          = "favicon.ico"
  source       = "favicon.ico"
  etag         = filemd5("favicon.ico")
  content_type = "image/x-icon"
}

resource "aws_route53_zone" "beneggerscom" {
  name = var.domainName
}

resource "aws_route53_record" "beneggerscom_a" {
  zone_id = aws_route53_zone.beneggerscom.zone_id
  name    = var.domainName
  type    = "A"
  alias {
    name                    = aws_s3_bucket.beneggerscom.website_domain
    zone_id                 = aws_s3_bucket.beneggerscom.hosted_zone_id
    evaluate_target_health  = false
  }
}

resource "aws_acm_certificate" "ssl_certificate" {
  provider                  = aws.acm_provider
  domain_name               = var.domainName
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate_validation" "ssl_certificate_validation" {
  provider                  = aws.acm_provider
  certificate_arn           = aws_acm_certificate.ssl_certificate.arn
  validation_record_fqdns   = [for record in aws_route53_record.ssl_certificate_validation : record.fqdn]
}

resource "aws_route53_record" "ssl_certificate_validation" {
  zone_id = aws_route53_zone.beneggerscom.zone_id
  name = element(aws_acm_certificate.ssl_certificate.domain_validation_options.*.resource_record_name, count.index)
  count = length(aws_acm_certificate.ssl_certificate.domain_validation_options)
  type = element(aws_acm_certificate.ssl_certificate.domain_validation_options.*.resource_record_type, count.index)
  records = [element(aws_acm_certificate.ssl_certificate.domain_validation_options.*.resource_record_value, count.index)]
  ttl = 60
}

resource "aws_route53_record" "protonmail_verification" {
  zone_id = aws_route53_zone.beneggerscom.zone_id
  name    = "_protomail-verification.beneggers.com"
  type    = "TXT"
  ttl     = "300"
  records = [
    "protonmail-verification=b5d34ec3d4e1bece3fcc6ab69f6df4cc986f1771",
    "v=spf1 include:_spf.protonmail.ch mx ~all"
  ]
}

resource "aws_route53_record" "protonmail_mx" {
  zone_id = aws_route53_zone.beneggerscom.zone_id
  name    = var.domainName
  type    = "MX"
  ttl     = "300"
  records = [
    "10 mail.protonmail.ch",
    "20 mailsec.protonmail.ch"
  ]
}

resource "aws_route53_record" "protonmail_dkim1" {
  zone_id = aws_route53_zone.beneggerscom.zone_id
  name    = "protonmail._domainkey"
  type    = "CNAME"
  ttl     = "300"
  records = [
    "protonmail.domainkey.dvpx6astltm7sml7dkxhvua4fjscroqq7y42ucsupvkrp5hpowzka.domains.proton.ch"
  ]
}

resource "aws_route53_record" "protonmail_dkim2" {
  zone_id = aws_route53_zone.beneggerscom.zone_id
  name    = "protonmail._domainkey2"
  type    = "CNAME"
  ttl     = "300"
  records = [
    "protonmail2.domainkey.dvpx6astltm7sml7dkxhvua4fjscroqq7y42ucsupvkrp5hpowzka.domains.proton.ch"
  ]
}

resource "aws_route53_record" "protonmail_dkim3" {
  zone_id = aws_route53_zone.beneggerscom.zone_id
  name    = "protonmail._domainkey3"
  type    = "CNAME"
  ttl     = "300"
  records = [
    "protonmail3.domainkey.dvpx6astltm7sml7dkxhvua4fjscroqq7y42ucsupvkrp5hpowzka.domains.proton.ch"
  ]
}