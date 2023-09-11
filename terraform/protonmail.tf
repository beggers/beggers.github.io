// This is technically DNS but logically distinct enough to warrant its own file.

resource "aws_route53_record" "protonmail_verification" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "_protomail-verification.beneggers.com"
  type    = "TXT"
  ttl     = "300"
  records = [
    "protonmail-verification=b5d34ec3d4e1bece3fcc6ab69f6df4cc986f1771",
    "v=spf1 include:_spf.protonmail.ch mx ~all"
  ]
}

resource "aws_route53_record" "protonmail_mx" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domainName
  type    = "MX"
  ttl     = "300"
  records = [
    "10 mail.protonmail.ch",
    "20 mailsec.protonmail.ch"
  ]
}

resource "aws_route53_record" "protonmail_dkim1" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "protonmail._domainkey"
  type    = "CNAME"
  ttl     = "300"
  records = [
    "protonmail.domainkey.dvpx6astltm7sml7dkxhvua4fjscroqq7y42ucsupvkrp5hpowzka.domains.proton.ch"
  ]
}

resource "aws_route53_record" "protonmail_dkim2" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "protonmail._domainkey2"
  type    = "CNAME"
  ttl     = "300"
  records = [
    "protonmail2.domainkey.dvpx6astltm7sml7dkxhvua4fjscroqq7y42ucsupvkrp5hpowzka.domains.proton.ch"
  ]
}

resource "aws_route53_record" "protonmail_dkim3" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "protonmail._domainkey3"
  type    = "CNAME"
  ttl     = "300"
  records = [
    "protonmail3.domainkey.dvpx6astltm7sml7dkxhvua4fjscroqq7y42ucsupvkrp5hpowzka.domains.proton.ch"
  ]
}