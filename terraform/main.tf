module "index" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = ["www.${var.domainName}"]
  file           = "index.html"
  file_directory = "../public/"
  fqdn           = var.domainName
  source_hash    = filemd5("../public/index.html")
  zone_id        = aws_route53_zone.main.zone_id
}
