resource "aws_route53_record" "fastmail_spf" {
  zone_id = aws_route53_zone.main.zone_id
  // Route53 only allows one TXT record. So, what, I can't
  // use DMARC?
  name    = var.domainName
  type    = "TXT"
  ttl     = "300"
  records = [
    "v=spf1 include:spf.messagingengine.com ?all",
  ]
}

resource "aws_route53_record" "fastmail_mx" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domainName
  type    = "MX"
  ttl     = "300"
  records = [
    "10 in1-smtp.messagingengine.com",
    "20 in2-smtp.messagingengine.com"
  ]
}

resource "aws_route53_record" "fastmail_dkim" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "fm1._domainkey.${var.domainName}"
  type    = "CNAME"
  ttl     = "300"
  records = [
    "fm1.${var.domainName}.dkim.fmhosted.com"
  ]
}

resource "aws_route53_record" "fastmail_dkim2" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "fm2._domainkey.${var.domainName}"
  type    = "CNAME"
  ttl     = "300"
  records = [
    "fm2.${var.domainName}.dkim.fmhosted.com"
  ]
}

resource "aws_route53_record" "fastmail_dkim3" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "fm3._domainkey.${var.domainName}"
  type    = "CNAME"
  ttl     = "300"
  records = [
    "fm3.${var.domainName}.dkim.fmhosted.com"
  ]
}