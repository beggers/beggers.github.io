resource "aws_route53_record" "fastmail_spf" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "beneggers.com"
  type    = "TXT"
  ttl     = "300"
  records = [
    "v=spf1 include:spf.messagingengine.com ?all",
  ]
}

resource "aws_route53_record" "fastmail_mx" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "beneggers.com"
  type    = "MX"
  ttl     = "300"
  records = [
    "10 in1-smtp.messagingengine.com",
    "20 in2-smtp.messagingengine.com"
  ]
}

resource "aws_route53_record" "fastmail_dkim" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "fm1._domainkey.beneggers.com"
  type    = "CNAME"
  ttl     = "300"
  records = [
    "fm1.beneggers.com.dkim.fmhosted.com"
  ]
}

resource "aws_route53_record" "fastmail_dkim2" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "fm2._domainkey.beneggers.com"
  type    = "CNAME"
  ttl     = "300"
  records = [
    "fm2.beneggers.com.dkim.fmhosted.com"
  ]
}

resource "aws_route53_record" "fastmail_dkim3" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "fm3._domainkey.beneggers.com"
  type    = "CNAME"
  ttl     = "300"
  records = [
    "fm3.beneggers.com.dkim.fmhosted.com"
  ]
}
