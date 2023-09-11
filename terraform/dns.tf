resource "aws_route53_zone" "main" {
  name = var.domainName
}

resource "aws_route53_record" "main_a" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domainName
  type    = "A"
  alias {
    name                    = aws_s3_bucket_website_configuration.main.website_domain
    zone_id                 = aws_s3_bucket.main.hosted_zone_id
    evaluate_target_health  = false
  }
}

resource "aws_acm_certificate" "main" {
  provider                  = aws.acm_provider
  domain_name               = var.domainName
  validation_method         = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate_validation" "main" {
  provider                  = aws.acm_provider
  certificate_arn           = aws_acm_certificate.main.arn
  validation_record_fqdns   = [for record in aws_route53_record.acm_validation : record.fqdn]
}

resource "aws_route53_record" "acm_validation" {
  zone_id = aws_route53_zone.main.zone_id
  name = element(aws_acm_certificate.main.domain_validation_options.*.resource_record_name, count.index)
  count = length(aws_acm_certificate.main.domain_validation_options)
  type = element(aws_acm_certificate.main.domain_validation_options.*.resource_record_type, count.index)
  records = [element(aws_acm_certificate.main.domain_validation_options.*.resource_record_value, count.index)]
  ttl = 60
}