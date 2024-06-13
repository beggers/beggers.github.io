resource "aws_route53_record" "a" {
  for_each = toset(concat([var.fqdn], var.domain_aliases))
  zone_id  = var.zone_id
  name     = each.value
  type     = "A"
  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "aaaa" {
  for_each = toset(concat([var.fqdn], var.domain_aliases))
  zone_id  = var.zone_id
  name     = each.value
  type     = "AAAA"
  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }
}
