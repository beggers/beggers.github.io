output "nameservers" {
  value = aws_route53_zone.main.name_servers
}

output "s3_bucket_id" {
  value = aws_s3_bucket.main.id
}

output "s3_website" {
  value = aws_s3_bucket_website_configuration.main.website_endpoint
}

output "s3_website_domain" {
  value = aws_s3_bucket_website_configuration.main.website_domain
}

output "s3_hosted_zone_id" {
  value = aws_s3_bucket.main.hosted_zone_id
}

output "s3_bucket_arn" {
  value = aws_s3_bucket.main.arn
}

output "acm_arn" {
  value = aws_acm_certificate.main.arn
}

output "acm_validation_id" {
  value = aws_acm_certificate_validation.main.id
}

output "acm_validation_fqdns" {
  value = aws_acm_certificate_validation.main.validation_record_fqdns
}

output "acm_validation_record_fqdns" {
  value = [for record in aws_route53_record.acm_validation : record.fqdn]
}

output "cloudfront_domain_name" {
  value = aws_cloudfront_distribution.main.domain_name
}

output "cloudfront_zone_id" {
  value = aws_cloudfront_distribution.main.hosted_zone_id
}

output "cloudfront_distribution_id" {
  value = aws_cloudfront_distribution.main.id
}
