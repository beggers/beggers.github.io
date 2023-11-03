output "cloudfront_distribution_id" {
  value = aws_cloudfront_distribution.main.id
}

output "hosted_zone_id" {
  value = aws_cloudfront_distribution.main.hosted_zone_id
}

output "bucket_id" {
  value = aws_s3_bucket.main.id
}

output "bucket_regional_domain_name" {
  value = aws_s3_bucket.main.bucket_regional_domain_name
}

output "cert_arn" {
  value = aws_acm_certificate.main.arn
}

output "cert_validation_record" {
  value = aws_acm_certificate_validation.main.validation_record_fqdns
}
