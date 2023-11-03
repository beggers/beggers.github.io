resource "aws_route53_zone" "main" {
  name = var.domainName
}

resource "aws_route53_record" "ns" {
  zone_id         = aws_route53_zone.main.zone_id
  name            = var.domainName
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

resource "aws_route53_record" "soa" {
  zone_id         = aws_route53_zone.main.zone_id
  name            = var.domainName
  type            = "SOA"
  ttl             = "900"
  allow_overwrite = true
  records = [
    "ns-578.awsdns-08.net. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 300"
  ]
}
