output "nameservers" {
  value = aws_route53_zone.main.name_servers
}

output "ptr_record" {
  value = aws_route53_record.ptr.records
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
