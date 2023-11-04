# This file is generated by the gen_tf.py script.
# Do not edit this file directly.

module "favicon" {
  source = "./zone_deployment"

  content_type   = "image/x-icon"
  domain_aliases = []
  file           = "favicon.ico"
  file_directory = "../pages/"
  fqdn           = "favicon.${var.domainName}"
  zone_id        = aws_route53_zone.main.zone_id
}

module "index" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = ["www.${var.domainName}"]
  file           = "index.html"
  file_directory = "../pages/"
  fqdn           = "${var.domainName}"
  zone_id        = aws_route53_zone.main.zone_id
}

module "about" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "about.html"
  file_directory = "../pages/"
  fqdn           = "about.${var.domainName}"
  zone_id        = aws_route53_zone.main.zone_id
}
