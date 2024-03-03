resource "aws_route53_zone" "main" {
  name = "beneggers.com"
}

resource "aws_route53_record" "ns" {
  zone_id         = aws_route53_zone.main.zone_id
  name            = "beneggers.com"
  type            = "NS"
  ttl             = "86400"
  allow_overwrite = true
  records = [
    aws_route53_zone.main.name_servers[0],
    aws_route53_zone.main.name_servers[1],
    aws_route53_zone.main.name_servers[2],
    aws_route53_zone.main.name_servers[3],
  ]
}

resource "aws_route53_record" "main_a" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "beneggers.com"
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "main_aaaa" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "beneggers.com"
  type    = "AAAA"
  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "www_a" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.beneggers.com"
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "www_aaaa" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.beneggers.com"
  type    = "AAAA"
  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "soa" {
  zone_id         = aws_route53_zone.main.zone_id
  name            = "beneggers.com"
  type            = "SOA"
  ttl             = "900"
  allow_overwrite = true
  records = [
    "ns-578.awsdns-08.net. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 300"
  ]
}
